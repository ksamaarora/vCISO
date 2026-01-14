# vciso-backend/app/services/gap_analyzer.py
from typing import List, Dict, Any
import logging
from datetime import datetime
from app.services.rag_service import RAGService
from app.core.llm_client import OpenAIClient
from app.models.gap_analysis import Gap, GapAnalysisResult, GapSeverity
import json

logger = logging.getLogger(__name__)

class GapAnalyzer:
    """Analyze IR plans against authoritative frameworks"""
    
    def __init__(self):
        self.rag_service = RAGService()
        self.llm_client = OpenAIClient()
    
    async def analyze_plan(
        self,
        plan_markdown: str,
        company_name: str
    ) -> GapAnalysisResult:
        """
        Perform comprehensive gap analysis on an IR plan
        
        Steps:
        1. Extract sections from the plan
        2. For each section, retrieve relevant framework guidance
        3. Use LLM to compare plan vs. guidance and identify gaps
        4. Aggregate results and calculate scores
        """
        logger.info(f"Starting gap analysis for: {company_name}")
        
        # Extract key sections from the plan
        sections = self._extract_plan_sections(plan_markdown)
        
        # Analyze each section
        all_gaps = []
        all_strengths = []
        
        for section_name, section_content in sections.items():
            section_gaps, section_strengths = await self._analyze_section(
                section_name=section_name,
                section_content=section_content
            )
            all_gaps.extend(section_gaps)
            all_strengths.extend(section_strengths)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(all_gaps)
        
        # Calculate per-framework compliance
        framework_compliance = self._calculate_framework_compliance(all_gaps)
        
        # Generate priority actions
        priority_actions = self._generate_priority_actions(all_gaps)
        
        return GapAnalysisResult(
            company_name=company_name,
            analysis_timestamp=datetime.utcnow().isoformat() + "Z",
            overall_score=overall_score,
            gaps=all_gaps,
            strengths=all_strengths,
            priority_actions=priority_actions,
            framework_compliance=framework_compliance
        )
    
    def _extract_plan_sections(self, plan_markdown: str) -> Dict[str, str]:
        """Extract sections from Markdown plan (naive implementation)"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in plan_markdown.split("\n"):
            # Check if line is a header (starts with ##)
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                
                # Start new section
                current_section = line.replace("##", "").strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content)
        
        return sections
    
    async def _analyze_section(
        self,
        section_name: str,
        section_content: str
    ) -> tuple[List[Gap], List[str]]:
        """Analyze a single section of the plan"""
        
        # Retrieve relevant framework guidance
        guidance_results = await self.rag_service.retrieve_relevant_guidance(
            query=f"{section_name}: {section_content[:500]}",  # Use first 500 chars for context
            top_k=5
        )
        
        # If no guidance found, skip analysis
        if not guidance_results:
            logger.warning(f"No guidance found for section: {section_name}")
            return [], []
        
        # Format guidance as context
        context = self.rag_service.format_retrieved_context(guidance_results)
        
        # Build prompt for LLM to identify gaps
        analysis_prompt = self._build_gap_analysis_prompt(
            section_name=section_name,
            section_content=section_content,
            framework_context=context
        )
        
        # Call LLM to analyze
        system_prompt = """You are a cybersecurity expert analyzing incident response plans against NIST, CISA, and SANS frameworks.

Your task is to identify gaps and strengths in the provided plan section.

Return your analysis as valid JSON with this structure:
{
  "gaps": [
    {
      "severity": "critical|high|medium|low",
      "description": "What's missing or inadequate",
      "recommendation": "Specific action to take",
      "framework_references": ["Citation 1", "Citation 2"],
      "estimated_effort": "Time estimate (e.g., '1-2 weeks')"
    }
  ],
  "strengths": [
    "What the plan does well (be specific)"
  ]
}

Guidelines:
- Only identify real gaps (compare against the framework context provided)
- Be specific in recommendations (not generic advice)
- Reference specific framework sections when possible
- Prioritize gaps by severity (critical = could lead to major incident failures)
"""
        
        try:
            response = await self.llm_client.generate_plan(
                system_prompt=system_prompt,
                user_prompt=analysis_prompt,
                temperature=0.3  # Lower temperature for more consistent analysis
            )
            
            # Parse JSON response
            analysis_result = json.loads(response)
            
            # Convert to Gap objects
            gaps = [
                Gap(
                    id=f"{section_name.lower().replace(' ', '-')}-gap-{idx}",
                    section=section_name,
                    severity=GapSeverity(gap_data["severity"]),
                    description=gap_data["description"],
                    recommendation=gap_data["recommendation"],
                    framework_references=gap_data["framework_references"],
                    estimated_effort=gap_data["estimated_effort"]
                )
                for idx, gap_data in enumerate(analysis_result.get("gaps", []))
            ]
            
            strengths = analysis_result.get("strengths", [])
            
            return gaps, strengths
            
        except Exception as e:
            logger.error(f"Error analyzing section {section_name}: {e}")
            return [], []
    
    def _build_gap_analysis_prompt(
        self,
        section_name: str,
        section_content: str,
        framework_context: str
    ) -> str:
        """Build prompt for gap analysis"""
        return f"""Analyze this IR plan section against framework guidance.

**Section: {section_name}**

**Current Plan Content:**
{section_content}

**Framework Guidance:**
{framework_context}

Identify:
1. Gaps (what's missing or inadequate)
2. Strengths (what's done well)

Be specific and actionable in your recommendations.
"""
    
    def _calculate_overall_score(self, gaps: List[Gap]) -> int:
        """Calculate overall compliance score (0-100)"""
        if not gaps:
            return 100
        
        # Weight by severity
        severity_weights = {
            GapSeverity.CRITICAL: 20,
            GapSeverity.HIGH: 10,
            GapSeverity.MEDIUM: 5,
            GapSeverity.LOW: 2
        }
        
        total_penalty = sum(severity_weights[gap.severity] for gap in gaps)
        score = max(0, 100 - total_penalty)
        
        return score
    
    def _calculate_framework_compliance(self, gaps: List[Gap]) -> Dict[str, int]:
        """Calculate compliance scores per framework"""
        # Extract framework mentions from gap references
        framework_scores = {"NIST": 100, "CISA": 100, "SANS": 100}
        
        for gap in gaps:
            for ref in gap.framework_references:
                if "NIST" in ref:
                    framework_scores["NIST"] -= 5
                if "CISA" in ref:
                    framework_scores["CISA"] -= 5
                if "SANS" in ref:
                    framework_scores["SANS"] -= 5
        
        # Ensure scores don't go below 0
        return {k: max(0, v) for k, v in framework_scores.items()}
    
    def _generate_priority_actions(self, gaps: List[Gap]) -> List[str]:
        """Generate top 3-5 priority actions from gaps"""
        # Sort by severity
        sorted_gaps = sorted(
            gaps,
            key=lambda g: {"critical": 0, "high": 1, "medium": 2, "low": 3}[g.severity]
        )
        
        # Take top 5 critical/high gaps
        priority_gaps = sorted_gaps[:5]
        
        return [gap.recommendation for gap in priority_gaps]