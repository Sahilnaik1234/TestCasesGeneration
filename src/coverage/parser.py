import xml.etree.ElementTree as ET
import os

class CoverageParser:
    def __init__(self, coverage_file_path: str):
        self.coverage_file_path = coverage_file_path

    def get_coverage_percentage(self) -> float:
        """
        Parses Cobertura coverage.xml or similarly formatted XML and returns the overall coverage percentage.
        Supports both Cobertura and Jacoco styles.
        """
        if not os.path.exists(self.coverage_file_path):
            raise FileNotFoundError(f"Coverage file not found at {self.coverage_file_path}")

        tree = ET.parse(self.coverage_file_path)
        root = tree.getroot()

        # Cobertura style
        if 'line-rate' in root.attrib:
            line_rate = float(root.attrib['line-rate'])
            return line_rate * 100.0

        # Jacoco style (if we see <report> and counters)
        if root.tag == 'report':
            for counter in root.findall('counter'):
                if counter.attrib.get('type') == 'LINE':
                    covered = float(counter.attrib.get('covered', 0))
                    missed = float(counter.attrib.get('missed', 0))
                    total = covered + missed
                    if total == 0:
                        return 0.0
                    return (covered / total) * 100.0

        # Add more parsers here if needed
        raise ValueError(f"Could not extract coverage percentage from {self.coverage_file_path}. format unknown.")

    def get_files_with_low_coverage(self, threshold: float) -> list:
        """
        Returns a list of dictionaries with file path and coverage info for files below the threshold.
        """
        tree = ET.parse(self.coverage_file_path)
        root = tree.getroot()
        low_coverage_files = []

        # Cobertura
        if 'line-rate' in root.attrib:
            for package in root.findall('.//package'):
                for cls in package.findall('.//class'):
                    line_rate = float(cls.attrib.get('line-rate', 0.0)) * 100
                    if line_rate < threshold:
                        low_coverage_files.append({
                            'filename': cls.attrib.get('filename', ''),
                            'coverage': line_rate
                        })
        return low_coverage_files
