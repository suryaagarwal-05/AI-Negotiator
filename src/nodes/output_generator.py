from src.state.state import State
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

class outputGenerator:
    def __init__(self, model):
        self.llm = model
        
    def process(self, state: State) -> dict:
        """
        Generate simple PDF from analyzer output
        """
        # Extract the analyzer output (last message should be from analyzer)
        analyzer_output = state["messages"][-1].content if state["messages"] else ""
        
        # Generate PDF
        pdf_path = self._generate_simple_pdf(analyzer_output)
        
        # Return the path to the generated PDF
        return {
            "messages": state["messages"] + [f"PDF report generated at: {pdf_path}"],
            "pdf_path": pdf_path
        }
    
    def _generate_simple_pdf(self, content: str) -> str:
        """Generate a simple PDF with just the content"""
        
        # Create output directory if it doesn't exist
        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        
        # Get basic style
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        
        # Create paragraph with the content
        story = [Paragraph(content.replace('\n', '<br/>'), normal_style)]
        
        # Build PDF
        doc.build(story)
        
        return filepath