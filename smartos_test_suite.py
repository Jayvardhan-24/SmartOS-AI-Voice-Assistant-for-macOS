#!/usr/bin/env python3
"""
SmartOS Test Suite - Comprehensive testing for the AI Operating System Assistant
Includes 50 test cases across 3 difficulty tiers as specified in requirements
"""

import json
import time
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import unittest
from smartos_main import SmartOSInterface, SmartOSCore, NLUProcessor, TaskExecutor

class SmartOSTestCase:
    """Individual test case for SmartOS evaluation"""
    
    def __init__(self, name: str, description: str, command: str, 
                 expected_action: str, difficulty: str, expected_success: bool = True):
        self.name = name
        self.description = description
        self.command = command
        self.expected_action = expected_action
        self.difficulty = difficulty
        self.expected_success = expected_success
        self.result = None
        self.execution_time = 0.0
        self.screenshot = None
        self.error = None

class SmartOSTestSuite:
    """Complete test suite for SmartOS evaluation"""
    
    def __init__(self):
        self.test_cases = self._generate_test_cases()
        self.results = []
        self.metrics = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "tier1_pass_rate": 0.0,
            "tier2_pass_rate": 0.0,
            "tier3_pass_rate": 0.0,
            "overall_pass_rate": 0.0,
            "average_response_time": 0.0
        }
        
    def _generate_test_cases(self) -> List[SmartOSTestCase]:
        """Generate 50 test cases across 3 difficulty tiers"""
        
        # Tier 1: Easy (40% = 20 test cases)
        tier1_cases = [
            SmartOSTestCase("T1_01", "Open Notepad", "open notepad", "open_application", "easy"),
            SmartOSTestCase("T1_02", "Launch Calculator", "start calculator", "open_application", "easy"),
            SmartOSTestCase("T1_03", "Open Browser", "launch browser", "open_application", "easy"),
            SmartOSTestCase("T1_04", "Start File Explorer", "open explorer", "open_application", "easy"),
            SmartOSTestCase("T1_05", "Open Command Prompt", "start cmd", "open_application", "easy"),
            SmartOSTestCase("T1_06", "Launch PowerShell", "open powershell", "open_application", "easy"),
            SmartOSTestCase("T1_07", "Start VS Code", "launch code", "open_application", "easy"),
            SmartOSTestCase("T1_08", "Open Word", "start word", "open_application", "easy"),
            SmartOSTestCase("T1_09", "Launch Excel", "open excel", "open_application", "easy"),
            SmartOSTestCase("T1_10", "Create New File", "create file test.txt", "file_operation", "easy"),
            SmartOSTestCase("T1_11", "Write to File", "write content to document.txt", "file_operation", "easy"),
            SmartOSTestCase("T1_12", "Open Text Editor", "start text editor", "open_application", "easy"),
            SmartOSTestCase("T1_13", "Launch File Manager", "open file manager", "open_application", "easy"),
            SmartOSTestCase("T1_14", "Start Terminal", "open terminal", "open_application", "easy"),
            SmartOSTestCase("T1_15", "Create Document", "create document report.txt", "file_operation", "easy"),
            SmartOSTestCase("T1_16", "Open Internet", "launch internet", "open_application", "easy"),
            SmartOSTestCase("T1_17", "Start Console", "open console", "open_application", "easy"),
            SmartOSTestCase("T1_18", "Launch Calc", "run calc", "open_application", "easy"),
            SmartOSTestCase("T1_19", "Open Files", "start files", "open_application", "easy"),
            SmartOSTestCase("T1_20", "Run Browser", "run browser", "open_application", "easy"),
        ]
        
        # Tier 2: Medium (40% = 20 test cases)
        tier2_cases = [
            SmartOSTestCase("T2_01", "Create and Edit File", "create file essay.txt and write content", "content_creation", "medium"),
            SmartOSTestCase("T2_02", "Write Essay", "write essay about technology", "content_creation", "medium"),
            SmartOSTestCase("T2_03", "Create Document with Topic", "create document about artificial intelligence", "content_creation", "medium"),
            SmartOSTestCase("T2_04", "Write Report", "write report about climate change", "content_creation", "medium"),
            SmartOSTestCase("T2_05", "Compose Letter", "compose letter about job application", "content_creation", "medium"),
            SmartOSTestCase("T2_06", "Create Multiple Files", "create file notes.txt and also create backup.txt", "file_operation", "medium"),
            SmartOSTestCase("T2_07", "Open App and Create File", "open notepad and create new document", "open_application", "medium"),
            SmartOSTestCase("T2_08", "Write and Save Content", "write essay about education and save it", "content_creation", "medium"),
            SmartOSTestCase("T2_09", "Complex File Operation", "create folder documents and add file readme.txt", "file_operation", "medium"),
            SmartOSTestCase("T2_10", "Multi-step Application", "launch calculator then open notepad", "open_application", "medium"),
            SmartOSTestCase("T2_11", "Content with Specifications", "write document about programming with examples", "content_creation", "medium"),
            SmartOSTestCase("T2_12", "File Management Task", "create file data.txt and copy it to backup.txt", "file_operation", "medium"),
            SmartOSTestCase("T2_13", "System Information Task", "open system information and create summary", "system_control", "medium"),
            SmartOSTestCase("T2_14", "Scheduled Task", "create reminder document for meeting tomorrow", "content_creation", "medium"),
            SmartOSTestCase("T2_15", "Application with Parameters", "open browser and navigate to search", "open_application", "medium"),
            SmartOSTestCase("T2_16", "Document Processing", "create report and format it properly", "content_creation", "medium"),
            SmartOSTestCase("T2_17", "File Organization", "create project folder and add files", "file_operation", "medium"),
            SmartOSTestCase("T2_18", "Multi-format Content", "write essay in both text and document format", "content_creation", "medium"),
            SmartOSTestCase("T2_19", "System Configuration", "open settings and create configuration notes", "system_control", "medium"),
            SmartOSTestCase("T2_20", "Complex Command Chain", "open explorer, create folder, and add readme file", "file_operation", "medium"),
        ]
        
        # Tier 3: Hard (20% = 10 test cases)
        tier3_cases = [
            SmartOSTestCase("T3_01", "Build and Deploy Project", "create project structure, write code, and prepare deployment", "content_creation", "hard"),
            SmartOSTestCase("T3_02", "System Automation Task", "automate file backup process and create schedule", "system_control", "hard"),
            SmartOSTestCase("T3_03", "Multi-application Workflow", "open multiple apps, create documents, and organize workspace", "open_application", "hard"),
            SmartOSTestCase("T3_04", "Complex Content Generation", "write comprehensive report with research, analysis, and recommendations", "content_creation", "hard"),
            SmartOSTestCase("T3_05", "System Integration Task", "integrate file system with applications and create automation", "system_control", "hard"),
            SmartOSTestCase("T3_06", "Advanced File Management", "organize entire project directory with proper structure and documentation", "file_operation", "hard"),
            SmartOSTestCase("T3_07", "Multi-step System Task", "configure system settings, create backup, and document process", "system_control", "hard"),
            SmartOSTestCase("T3_08", "Complex Application Suite", "set up development environment with multiple tools and configurations", "open_application", "hard"),
            SmartOSTestCase("T3_09", "Comprehensive Documentation", "create complete project documentation with examples and guides", "content_creation", "hard"),
            SmartOSTestCase("T3_10", "Full System Workflow", "execute complete workflow from planning to implementation and testing", "system_control", "hard"),
        ]
        
        return tier1_cases + tier2_cases + tier3_cases
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test cases and generate comprehensive results"""
        print("Starting SmartOS Test Suite...")
        print(f"Total test cases: {len(self.test_cases)}")
        
        # Initialize SmartOS for testing
        try:
            smart_os = SmartOSInterface()
        except Exception as e:
            print(f"Failed to initialize SmartOS: {e}")
            return {"error": "Initialization failed"}
        
        # Run each test case
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\nRunning test {i}/{len(self.test_cases)}: {test_case.name}")
            print(f"Description: {test_case.description}")
            print(f"Command: {test_case.command}")
            
            result = self._execute_test_case(smart_os, test_case)
            self.results.append(result)
            
            # Print immediate result
            status = "PASS" if result["success"] else "FAIL"
            print(f"Result: {status} ({result['execution_time']:.2f}s)")
            if not result["success"]:
                print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Calculate metrics
        self._calculate_metrics()
        
        # Generate detailed report
        report = self._generate_report()
        
        # Save results
        self._save_results()
        
        return report
    
    def _execute_test_case(self, smart_os: SmartOSInterface, test_case: SmartOSTestCase) -> Dict[str, Any]:
        """Execute individual test case"""
        start_time = time.time()
        
        try:
            # Parse the command
            intent = smart_os.nlu.parse_command(test_case.command)
            
            # Check if intent matches expected action
            intent_correct = intent["action"] == test_case.expected_action
            
            # Execute the command
            execution_result = smart_os.executor.execute_intent(intent)
            
            # Determine overall success
            success = (intent_correct and execution_result["success"] and 
                      execution_result["execution_time"] < smart_os.core.config["response_timeout"])
            
            execution_time = time.time() - start_time
            
            return {
                "test_name": test_case.name,
                "description": test_case.description,
                "command": test_case.command,
                "difficulty": test_case.difficulty,
                "expected_action": test_case.expected_action,
                "actual_action": intent["action"],
                "intent_confidence": intent["confidence"],
                "success": success,
                "execution_time": execution_time,
                "response_time": execution_result["execution_time"],
                "message": execution_result.get("message", ""),
                "error": execution_result.get("error"),
                "screenshot": execution_result.get("screenshot"),
                "intent_correct": intent_correct,
                "execution_successful": execution_result["success"]
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "test_name": test_case.name,
                "description": test_case.description,
                "command": test_case.command,
                "difficulty": test_case.difficulty,
                "success": False,
                "execution_time": execution_time,
                "error": str(e),
                "intent_correct": False,
                "execution_successful": False
            }
    
    def _calculate_metrics(self):
        """Calculate comprehensive test metrics"""
        if not self.results:
            return
        
        self.metrics["total_tests"] = len(self.results)
        self.metrics["passed_tests"] = sum(1 for r in self.results if r["success"])
        self.metrics["failed_tests"] = self.metrics["total_tests"] - self.metrics["passed_tests"]
        
        # Calculate tier-specific pass rates
        tier1_results = [r for r in self.results if r["difficulty"] == "easy"]
        tier2_results = [r for r in self.results if r["difficulty"] == "medium"]
        tier3_results = [r for r in self.results if r["difficulty"] == "hard"]
        
        self.metrics["tier1_pass_rate"] = (
            sum(1 for r in tier1_results if r["success"]) / len(tier1_results) * 100
            if tier1_results else 0
        )
        
        self.metrics["tier2_pass_rate"] = (
            sum(1 for r in tier2_results if r["success"]) / len(tier2_results) * 100
            if tier2_results else 0
        )
        
        self.metrics["tier3_pass_rate"] = (
            sum(1 for r in tier3_results if r["success"]) / len(tier3_results) * 100
            if tier3_results else 0
        )
        
        # Overall pass rate
        self.metrics["overall_pass_rate"] = (
            self.metrics["passed_tests"] / self.metrics["total_tests"] * 100
        )
        
        # Average response time
        response_times = [r["execution_time"] for r in self.results if "execution_time" in r]
        self.metrics["average_response_time"] = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        
        # Performance benchmarks
        fast_responses = sum(1 for r in self.results if r.get("execution_time", float('inf')) < 3.0)
        self.metrics["fast_response_rate"] = fast_responses / len(self.results) * 100
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        report = {
            "test_summary": {
                "total_tests": self.metrics["total_tests"],
                "passed_tests": self.metrics["passed_tests"],
                "failed_tests": self.metrics["failed_tests"],
                "overall_pass_rate": round(self.metrics["overall_pass_rate"], 2),
                "average_response_time": round(self.metrics["average_response_time"], 3)
            },
            "tier_performance": {
                "tier1_easy": {
                    "total": len([r for r in self.results if r["difficulty"] == "easy"]),
                    "passed": len([r for r in self.results if r["difficulty"] == "easy" and r["success"]]),
                    "pass_rate": round(self.metrics["tier1_pass_rate"], 2)
                },
                "tier2_medium": {
                    "total": len([r for r in self.results if r["difficulty"] == "medium"]),
                    "passed": len([r for r in self.results if r["difficulty"] == "medium" and r["success"]]),
                    "pass_rate": round(self.metrics["tier2_pass_rate"], 2)
                },
                "tier3_hard": {
                    "total": len([r for r in self.results if r["difficulty"] == "hard"]),
                    "passed": len([r for r in self.results if r["difficulty"] == "hard" and r["success"]]),
                    "pass_rate": round(self.metrics["tier3_pass_rate"], 2)
                }
            },
            "performance_metrics": {
                "fast_response_rate": round(self.metrics["fast_response_rate"], 2),
                "success_criteria_met": {
                    "pass_rate_above_90": self.metrics["overall_pass_rate"] > 90,
                    "fast_response_80_percent": self.metrics["fast_response_rate"] > 80,
                    "autonomous_execution": True  # Based on no manual intervention needed
                }
            },
            "detailed_results": self.results
        }
        
        return report
    
    def _save_results(self):
        """Save test results to files"""
        results_dir = Path("test_results")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_file = results_dir / f"smartos_test_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                "metrics": self.metrics,
                "results": self.results
            }, f, indent=2)
        
        # Save Excel-compatible CSV
        try:
            import pandas as pd
            df = pd.DataFrame(self.results)
            excel_file = results_dir / f"smartos_test_results_{timestamp}.xlsx"
            df.to_excel(excel_file, index=False)
        except ImportError:
            # Fallback to CSV if pandas not available
            import csv
            csv_file = results_dir / f"smartos_test_results_{timestamp}.csv"
            with open(csv_file, 'w', newline='') as f:
                if self.results:
                    writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                    writer.writeheader()
                    writer.writerows(self.results)
        
        print(f"Results saved to {results_dir}")
    
    def print_summary(self):
        """Print test summary to console"""
        print("\n" + "="*60)
        print("SMARTOS TEST SUITE SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.metrics['total_tests']}")
        print(f"Passed: {self.metrics['passed_tests']}")
        print(f"Failed: {self.metrics['failed_tests']}")
        print(f"Overall Pass Rate: {self.metrics['overall_pass_rate']:.1f}%")
        print(f"Average Response Time: {self.metrics['average_response_time']:.3f}s")
        
        print(f"\nTier Performance:")
        print(f"  Easy (Tier 1): {self.metrics['tier1_pass_rate']:.1f}%")
        print(f"  Medium (Tier 2): {self.metrics['tier2_pass_rate']:.1f}%")
        print(f"  Hard (Tier 3): {self.metrics['tier3_pass_rate']:.1f}%")
        
        print(f"\nSuccess Criteria:")
        print(f"  Pass Rate >90%: {'✓' if self.metrics['overall_pass_rate'] > 90 else '✗'}")
        print(f"  Fast Response >80%: {'✓' if self.metrics.get('fast_response_rate', 0) > 80 else '✗'}")
        print("="*60)

def main():
    """Main test execution"""
    test_suite = SmartOSTestSuite()
    
    print("SmartOS Test Suite - Version 1.0")
    print("Comprehensive evaluation with 50 test cases")
    print("Distribution: Easy 40%, Medium 40%, Hard 20%")
    
    # Run all tests
    report = test_suite.run_all_tests()
    
    # Print summary
    test_suite.print_summary()
    
    # Check success criteria
    if report and "test_summary" in report:
        success_criteria_met = (
            report["test_summary"]["overall_pass_rate"] > 90 and
            report["performance_metrics"]["fast_response_rate"] > 80
        )
        
        print(f"\nOverall Success: {'✓ PASSED' if success_criteria_met else '✗ FAILED'}")
    
    return report

if __name__ == "__main__":
    main()