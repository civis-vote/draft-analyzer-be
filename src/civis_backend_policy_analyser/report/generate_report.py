import os

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from weasyprint import HTML

from civis_backend_policy_analyser.schemas.document_report_schema import ReportRequest


class ReportGenerator:
    def __init__(self, template_dir: str = "templates", output_dir: str = "reports"):
        self.template_dir = template_dir
        self.output_dir = output_dir

        logger.info("Initializing ReportGenerator...")
        os.makedirs(self.output_dir, exist_ok=True)

        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.template = self.env.get_template("assessment_template.html")
        self.cover_template = self.env.get_template("cover_template.html")
        self.base_template = self.env.get_template("base_template.html")
        logger.info("Templates loaded successfully")

    def generate_combined_report(self, request: ReportRequest, filename: str = "final_report.pdf") -> str:
        """
        Generates a multi-page PDF report using a ReportRequest object.
        
        Args:
            request: ReportRequest object containing cover and assessments
            filename: Optional filename for the PDF

        Returns:
            Path to the generated PDF
        """
        try:
            logger.info("Generating cover page from ReportRequest...")

            output_path = os.path.join(self.output_dir, filename)
            logger.info(f"Generating PDF at: {output_path}")
            cover_html = self.cover_template.render(**request.cover.dict())

            body_html = ""

            for assessment in request.assessments:
                body_html += self.template.render(**assessment.dict())

            # Combine and wrap in the base layout
            full_html = self.base_template.render(content=cover_html + body_html)

            HTML(string=full_html).write_pdf(output_path)

            logger.info(f"Final multi-page report generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating combined report: {e}")
            raise
