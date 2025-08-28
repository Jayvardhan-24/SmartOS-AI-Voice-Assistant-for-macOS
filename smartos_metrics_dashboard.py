#!/usr/bin/env python3
"""
SmartOS Metrics Dashboard - Performance monitoring and evaluation framework
Provides comprehensive metrics visualization and real-time monitoring
"""

import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import threading
import logging

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.animation import FuncAnimation
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class MetricsCollector:
    """Collect and aggregate SmartOS performance metrics"""
    
    def __init__(self, data_dir: str = "execution_logs"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.metrics_cache = {}
        self.real_time_metrics = {
            "commands_per_minute": 0,
            "average_response_time": 0.0,
            "success_rate": 0.0,
            "active_sessions": 0,
            "memory_usage": 0.0,
            "cpu_usage": 0.0
        }
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for metrics collection"""
        logger = logging.getLogger("MetricsCollector")
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler("logs/metrics.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def collect_execution_data(self) -> List[Dict]:
        """Collect all execution data from log files"""
        all_data = []
        
        for log_file in self.data_dir.glob("execution_*.json"):
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)
            except Exception as e:
                self.logger.error(f"Error reading {log_file}: {e}")
        
        return all_data
    
    def calculate_performance_metrics(self, data: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics"""
        if not data:
            return {}
        
        # Basic metrics
        total_commands = len(data)
        successful_commands = sum(1 for d in data if d.get('result', {}).get('success', False))
        failed_commands = total_commands - successful_commands
        
        # Response time metrics
        response_times = [d.get('execution_time', 0) for d in data if 'execution_time' in d]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Success rate by time periods
        now = datetime.now()
        last_hour = [d for d in data if self._within_timeframe(d, hours=1)]
        last_day = [d for d in data if self._within_timeframe(d, hours=24)]
        
        # Intent accuracy
        correct_intents = sum(1 for d in data if d.get('intent', {}).get('confidence', 0) > 0.8)
        intent_accuracy = (correct_intents / total_commands * 100) if total_commands > 0 else 0
        
        # Command categories
        command_categories = {}
        for d in data:
            action = d.get('intent', {}).get('action', 'unknown')
            command_categories[action] = command_categories.get(action, 0) + 1
        
        # Performance by category
        category_performance = {}
        for category in command_categories:
            category_data = [d for d in data if d.get('intent', {}).get('action') == category]
            category_success = sum(1 for d in category_data if d.get('result', {}).get('success', False))
            category_performance[category] = {
                'total': len(category_data),
                'success': category_success,
                'success_rate': (category_success / len(category_data) * 100) if category_data else 0,
                'avg_response_time': sum(d.get('execution_time', 0) for d in category_data) / len(category_data) if category_data else 0
            }
        
        return {
            'overview': {
                'total_commands': total_commands,
                'successful_commands': successful_commands,
                'failed_commands': failed_commands,
                'success_rate': (successful_commands / total_commands * 100) if total_commands > 0 else 0,
                'average_response_time': avg_response_time,
                'intent_accuracy': intent_accuracy
            },
            'time_based': {
                'last_hour': {
                    'total': len(last_hour),
                    'success_rate': (sum(1 for d in last_hour if d.get('result', {}).get('success', False)) / len(last_hour) * 100) if last_hour else 0
                },
                'last_day': {
                    'total': len(last_day),
                    'success_rate': (sum(1 for d in last_day if d.get('result', {}).get('success', False)) / len(last_day) * 100) if last_day else 0
                }
            },
            'categories': command_categories,
            'performance_by_category': category_performance,
            'response_time_distribution': {
                'under_1s': sum(1 for t in response_times if t < 1.0),
                'under_3s': sum(1 for t in response_times if t < 3.0),
                'under_5s': sum(1 for t in response_times if t < 5.0),
                'over_5s': sum(1 for t in response_times if t >= 5.0)
            }
        }
    
    def _within_timeframe(self, data_point: Dict, hours: int) -> bool:
        """Check if data point is within specified timeframe"""
        try:
            timestamp_str = data_point.get('timestamp', '')
            if not timestamp_str:
                return False
            
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            cutoff = datetime.now() - timedelta(hours=hours)
            return timestamp >= cutoff
        except Exception:
            return False

class DashboardGenerator:
    """Generate visual dashboard for SmartOS metrics"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.collector = metrics_collector
        self.output_dir = Path("dashboard")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_html_dashboard(self, metrics: Dict[str, Any]) -> str:
        """Generate HTML dashboard"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartOS Metrics Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        .metric-title {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .metric-subtitle {
            font-size: 12px;
            color: #888;
        }
        .success { border-left-color: #4CAF50; }
        .warning { border-left-color: #FF9800; }
        .error { border-left-color: #F44336; }
        .info { border-left-color: #2196F3; }
        
        .chart-container {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .progress-bar {
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            margin: 10px 0;
        }
        .progress-fill {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            height: 100%;
            transition: width 0.3s ease;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-success { background-color: #4CAF50; }
        .status-warning { background-color: #FF9800; }
        .status-error { background-color: #F44336; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>SmartOS Metrics Dashboard</h1>
            <p>Real-time performance monitoring and analytics</p>
            <p>Last Updated: {timestamp}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card success">
                <div class="metric-title">Success Rate</div>
                <div class="metric-value">{success_rate:.1f}%</div>
                <div class="metric-subtitle">Overall command success rate</div>
            </div>
            
            <div class="metric-card info">
                <div class="metric-title">Total Commands</div>
                <div class="metric-value">{total_commands:,}</div>
                <div class="metric-subtitle">Commands processed</div>
            </div>
            
            <div class="metric-card warning">
                <div class="metric-title">Avg Response Time</div>
                <div class="metric-value">{avg_response_time:.2f}s</div>
                <div class="metric-subtitle">Average execution time</div>
            </div>
            
            <div class="metric-card info">
                <div class="metric-title">Intent Accuracy</div>
                <div class="metric-value">{intent_accuracy:.1f}%</div>
                <div class="metric-subtitle">Command understanding rate</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Performance Targets</h3>
            <div>
                <label>Success Rate Target (>90%)</label>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {success_rate}%"></div>
                </div>
                <small>{success_rate:.1f}% / 90%</small>
            </div>
            
            <div>
                <label>Fast Response Target (<3s for 80%)</label>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {fast_response_rate}%"></div>
                </div>
                <small>{fast_response_rate:.1f}% under 3 seconds</small>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Command Categories Performance</h3>
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Total Commands</th>
                        <th>Success Rate</th>
                        <th>Avg Response Time</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {category_rows}
                </tbody>
            </table>
        </div>
        
        <div class="chart-container">
            <h3>Response Time Distribution</h3>
            <canvas id="responseTimeChart" width="400" height="200"></canvas>
        </div>
        
        <div class="chart-container">
            <h3>System Health</h3>
            <div class="metrics-grid">
                <div>
                    <span class="status-indicator status-{health_status}"></span>
                    <strong>Overall Health: {health_status_text}</strong>
                </div>
                <div>Success Rate: {success_rate:.1f}%</div>
                <div>Response Time: {avg_response_time:.2f}s</div>
                <div>Intent Accuracy: {intent_accuracy:.1f}%</div>
            </div>
        </div>
    </div>
    
    <script>
        // Response Time Distribution Chart
        const ctx = document.getElementById('responseTimeChart').getContext('2d');
        const responseTimeChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['< 1s', '1-3s', '3-5s', '> 5s'],
                datasets: [{{
                    data: [{under_1s}, {under_1to3s}, {under_3to5s}, {over_5s}],
                    backgroundColor: [
                        '#4CAF50',
                        '#8BC34A', 
                        '#FF9800',
                        '#F44336'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Auto-refresh every 30 seconds
        setTimeout(function() {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>
"""
        
        # Calculate additional metrics
        overview = metrics.get('overview', {})
        response_dist = metrics.get('response_time_distribution', {})
        categories = metrics.get('performance_by_category', {})
        
        fast_response_rate = ((response_dist.get('under_1s', 0) + response_dist.get('under_3s', 0)) / 
                             overview.get('total_commands', 1) * 100) if overview.get('total_commands', 0) > 0 else 0
        
        # Generate category rows
        category_rows = ""
        for category, perf in categories.items():
            status = "success" if perf['success_rate'] > 80 else "warning" if perf['success_rate'] > 60 else "error"
            status_text = "Good" if perf['success_rate'] > 80 else "Fair" if perf['success_rate'] > 60 else "Poor"
            
            category_rows += f"""
            <tr>
                <td>{category.replace('_', ' ').title()}</td>
                <td>{perf['total']}</td>
                <td>{perf['success_rate']:.1f}%</td>
                <td>{perf['avg_response_time']:.2f}s</td>
                <td><span class="status-indicator status-{status}"></span>{status_text}</td>
            </tr>
            """
        
        # Overall health status
        success_rate = overview.get('success_rate', 0)
        health_status = "success" if success_rate > 80 else "warning" if success_rate > 60 else "error"
        health_status_text = "Excellent" if success_rate > 90 else "Good" if success_rate > 80 else "Fair" if success_rate > 60 else "Poor"
        
        # Fill template
        html_content = html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            success_rate=overview.get('success_rate', 0),
            total_commands=overview.get('total_commands', 0),
            avg_response_time=overview.get('average_response_time', 0),
            intent_accuracy=overview.get('intent_accuracy', 0),
            fast_response_rate=fast_response_rate,
            category_rows=category_rows,
            health_status=health_status,
            health_status_text=health_status_text,
            under_1s=response_dist.get('under_1s', 0),
            under_1to3s=response_dist.get('under_3s', 0) - response_dist.get('under_1s', 0),
            under_3to5s=response_dist.get('under_5s', 0) - response_dist.get('under_3s', 0),
            over_5s=response_dist.get('over_5s', 0)
        )
        
        return html_content
    
    def save_dashboard(self, html_content: str) -> str:
        """Save HTML dashboard to file"""
        dashboard_file = self.output_dir / f"smartos_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        with open(dashboard_file, 'w') as f:
            f.write(html_content)
        
        # Also save as latest
        latest_file = self.output_dir / "smartos_dashboard_latest.html"
        with open(latest_file, 'w') as f:
            f.write(html_content)
        
        return str(dashboard_file)

class RealTimeMonitor:
    """Real-time monitoring system for SmartOS"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.collector = metrics_collector
        self.dashboard_generator = DashboardGenerator(metrics_collector)
        self.monitoring = False
        self.monitor_thread = None
        self.update_interval = 60  # seconds
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        
        print("Real-time monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect latest data
                execution_data = self.collector.collect_execution_data()
                
                # Calculate metrics
                metrics = self.collector.calculate_performance_metrics(execution_data)
                
                # Generate dashboard
                html_content = self.dashboard_generator.generate_html_dashboard(metrics)
                dashboard_file = self.dashboard_generator.save_dashboard(html_content)
                
                # Log metrics
                self.collector.logger.info(f"Metrics updated: {len(execution_data)} commands processed")
                
                # Wait for next update
                time.sleep(self.update_interval)
                
            except Exception as e:
                self.collector.logger.error(f"Monitoring error: {e}")
                time.sleep(self.update_interval)

def main():
    """Main dashboard generator"""
    print("SmartOS Metrics Dashboard Generator")
    print("=" * 40)
    
    # Initialize components
    collector = MetricsCollector()
    dashboard_gen = DashboardGenerator(collector)
    monitor = RealTimeMonitor(collector)
    
    try:
        # Collect current data
        print("Collecting execution data...")
        execution_data = collector.collect_execution_data()
        print(f"Found {len(execution_data)} execution records")
        
        if not execution_data:
            print("No execution data found. Run SmartOS commands first to generate metrics.")
            return
        
        # Calculate metrics
        print("Calculating performance metrics...")
        metrics = collector.calculate_performance_metrics(execution_data)
        
        # Generate dashboard
        print("Generating HTML dashboard...")
        html_content = dashboard_gen.generate_html_dashboard(metrics)
        dashboard_file = dashboard_gen.save_dashboard(html_content)
        
        print(f"Dashboard generated: {dashboard_file}")
        print(f"Open {dashboard_gen.output_dir / 'smartos_dashboard_latest.html'} in your browser")
        
        # Display key metrics
        overview = metrics.get('overview', {})
        print(f"\nKey Metrics:")
        print(f"  Success Rate: {overview.get('success_rate', 0):.1f}%")
        print(f"  Total Commands: {overview.get('total_commands', 0)}")
        print(f"  Average Response Time: {overview.get('average_response_time', 0):.2f}s")
        print(f"  Intent Accuracy: {overview.get('intent_accuracy', 0):.1f}%")
        
        # Ask for real-time monitoring
        choice = input("\nStart real-time monitoring? (y/n): ").lower()
        if choice == 'y':
            monitor.start_monitoring()
            print("Monitoring started. Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                print("Monitoring stopped.")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())