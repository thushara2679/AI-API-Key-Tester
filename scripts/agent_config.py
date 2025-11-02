#!/usr/bin/env python3

"""
agent_config.py - Agent Configuration Utility

Purpose: Manage and configure agents in the Advanced AI Agent System
Usage: python3 agent_config.py [command] [options]

Commands:
  init       - Initialize agent configuration
  list       - List all agents
  create     - Create new agent
  update     - Update agent configuration
  validate   - Validate agent configuration
  export     - Export configuration
  import     - Import configuration

Features:
- Create and manage agent configs
- Validate agent specifications
- Generate documentation
- Export/import configurations
"""

import json
import sys
import argparse
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(msg: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_success(msg: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_warning(msg: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_error(msg: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {msg}")

class AgentConfig:
    """Agent configuration and management"""
    
    def __init__(self, config_dir: str = ".agents"):
        """Initialize agent configuration manager"""
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
    def create_default_config(self, agent_name: str) -> Dict[str, Any]:
        """Create default agent configuration"""
        return {
            'name': agent_name,
            'version': '1.0.0',
            'type': 'worker',
            'description': f'Agent: {agent_name}',
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'capabilities': [],
            'dependencies': [],
            'configuration': {
                'timeout': 30,
                'retries': 3,
                'max_workers': 5,
                'logging': {
                    'level': 'INFO',
                    'format': 'structured'
                }
            },
            'environment': {
                'development': {},
                'staging': {},
                'production': {}
            },
            'interfaces': {
                'input': [],
                'output': []
            }
        }
    
    def validate_agent_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate agent configuration"""
        errors = []
        
        # Required fields
        required_fields = ['name', 'version', 'type', 'description']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate name
        if 'name' in config:
            if not re.match(r'^[a-z0-9_-]+$', config['name']):
                errors.append("Agent name must contain only lowercase letters, numbers, hyphens, and underscores")
        
        # Validate version
        if 'version' in config:
            if not re.match(r'^\d+\.\d+\.\d+$', config['version']):
                errors.append("Version must follow semantic versioning (x.y.z)")
        
        # Validate type
        valid_types = ['worker', 'coordinator', 'validator', 'transformer', 'aggregator']
        if 'type' in config:
            if config['type'] not in valid_types:
                errors.append(f"Invalid agent type. Must be one of: {', '.join(valid_types)}")
        
        # Validate configuration
        if 'configuration' in config:
            config_obj = config['configuration']
            if 'timeout' in config_obj:
                if not isinstance(config_obj['timeout'], (int, float)) or config_obj['timeout'] <= 0:
                    errors.append("Timeout must be positive number")
            
            if 'retries' in config_obj:
                if not isinstance(config_obj['retries'], int) or config_obj['retries'] < 0:
                    errors.append("Retries must be non-negative integer")
        
        return len(errors) == 0, errors
    
    def save_agent(self, agent_name: str, config: Dict[str, Any]) -> bool:
        """Save agent configuration to file"""
        config_file = self.config_dir / f"{agent_name}.yaml"
        
        try:
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            print_success(f"Saved: {config_file}")
            return True
        except Exception as e:
            print_error(f"Failed to save configuration: {e}")
            return False
    
    def load_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Load agent configuration from file"""
        config_file = self.config_dir / f"{agent_name}.yaml"
        
        if not config_file.exists():
            print_error(f"Agent not found: {agent_name}")
            return None
        
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print_error(f"Failed to load configuration: {e}")
            return None
    
    def list_agents(self) -> List[str]:
        """List all configured agents"""
        agents = []
        for config_file in self.config_dir.glob("*.yaml"):
            agents.append(config_file.stem)
        return sorted(agents)
    
    def delete_agent(self, agent_name: str) -> bool:
        """Delete agent configuration"""
        config_file = self.config_dir / f"{agent_name}.yaml"
        
        if not config_file.exists():
            print_error(f"Agent not found: {agent_name}")
            return False
        
        try:
            config_file.unlink()
            print_success(f"Deleted: {agent_name}")
            return True
        except Exception as e:
            print_error(f"Failed to delete agent: {e}")
            return False
    
    def export_agents(self, output_file: str = None) -> bool:
        """Export all agent configurations"""
        agents = {}
        
        for agent_name in self.list_agents():
            config = self.load_agent(agent_name)
            if config:
                agents[agent_name] = config
        
        if not agents:
            print_warning("No agents to export")
            return False
        
        output = {
            'exported_at': datetime.now().isoformat(),
            'count': len(agents),
            'agents': agents
        }
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(output, f, indent=2)
                print_success(f"Exported {len(agents)} agents to {output_file}")
                return True
            except Exception as e:
                print_error(f"Failed to export: {e}")
                return False
        else:
            print(json.dumps(output, indent=2))
            return True
    
    def import_agents(self, input_file: str) -> bool:
        """Import agent configurations"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            print_error(f"Import file not found: {input_file}")
            return False
        
        try:
            with open(input_path, 'r') as f:
                data = json.load(f)
            
            if 'agents' not in data:
                print_error("Invalid import file format")
                return False
            
            imported_count = 0
            for agent_name, config in data['agents'].items():
                is_valid, errors = self.validate_agent_config(config)
                if not is_valid:
                    print_warning(f"Skipping invalid agent {agent_name}: {errors}")
                    continue
                
                if self.save_agent(agent_name, config):
                    imported_count += 1
            
            print_success(f"Imported {imported_count} agents")
            return imported_count > 0
        except Exception as e:
            print_error(f"Failed to import: {e}")
            return False
    
    def generate_documentation(self, agent_name: str) -> str:
        """Generate documentation for agent"""
        config = self.load_agent(agent_name)
        if not config:
            return ""
        
        doc = []
        doc.append(f"# Agent: {config['name']}\n")
        doc.append(f"**Version:** {config['version']}\n")
        doc.append(f"**Type:** {config['type']}\n")
        doc.append(f"**Description:** {config['description']}\n")
        
        if config.get('capabilities'):
            doc.append("\n## Capabilities\n")
            for capability in config['capabilities']:
                doc.append(f"- {capability}")
        
        if config.get('dependencies'):
            doc.append("\n## Dependencies\n")
            for dependency in config['dependencies']:
                doc.append(f"- {dependency}")
        
        doc.append("\n## Configuration\n")
        doc.append("```yaml")
        doc.append(yaml.dump(config.get('configuration', {}), default_flow_style=False))
        doc.append("```")
        
        if config.get('interfaces'):
            doc.append("\n## Interfaces\n")
            interfaces = config['interfaces']
            if interfaces.get('input'):
                doc.append("\n### Input\n")
                for inp in interfaces['input']:
                    doc.append(f"- {inp}")
            if interfaces.get('output'):
                doc.append("\n### Output\n")
                for out in interfaces['output']:
                    doc.append(f"- {out}")
        
        return "\n".join(doc)

class AgentConfigCLI:
    """Command-line interface for agent configuration"""
    
    def __init__(self):
        """Initialize CLI"""
        self.agent_config = AgentConfig()
    
    def cmd_init(self, args) -> int:
        """Initialize new agent"""
        config = self.agent_config.create_default_config(args.name)
        
        is_valid, errors = self.agent_config.validate_agent_config(config)
        if not is_valid:
            for error in errors:
                print_error(error)
            return 1
        
        if self.agent_config.save_agent(args.name, config):
            print_success(f"Created agent: {args.name}")
            return 0
        return 1
    
    def cmd_list(self, args) -> int:
        """List all agents"""
        agents = self.agent_config.list_agents()
        
        if not agents:
            print_warning("No agents configured")
            return 0
        
        print(f"\n{Colors.BOLD}Configured Agents ({len(agents)}){Colors.END}\n")
        
        for agent_name in agents:
            config = self.agent_config.load_agent(agent_name)
            if config:
                print(f"  {Colors.GREEN}•{Colors.END} {config['name']}")
                print(f"    Type: {config.get('type', 'unknown')}")
                print(f"    Version: {config.get('version', 'unknown')}")
        
        print()
        return 0
    
    def cmd_create(self, args) -> int:
        """Create new agent"""
        config = self.agent_config.create_default_config(args.name)
        
        # Allow customization
        if args.type:
            config['type'] = args.type
        if args.description:
            config['description'] = args.description
        
        is_valid, errors = self.agent_config.validate_agent_config(config)
        if not is_valid:
            for error in errors:
                print_error(error)
            return 1
        
        if self.agent_config.save_agent(args.name, config):
            print_success(f"Created agent: {args.name}")
            return 0
        return 1
    
    def cmd_validate(self, args) -> int:
        """Validate agent configuration"""
        config = self.agent_config.load_agent(args.name)
        if not config:
            return 1
        
        is_valid, errors = self.agent_config.validate_agent_config(config)
        
        if is_valid:
            print_success(f"Agent configuration is valid: {args.name}")
            return 0
        else:
            print_error(f"Agent configuration is invalid: {args.name}")
            for error in errors:
                print(f"  - {error}")
            return 1
    
    def cmd_export(self, args) -> int:
        """Export configurations"""
        return 0 if self.agent_config.export_agents(args.output) else 1
    
    def cmd_import(self, args) -> int:
        """Import configurations"""
        return 0 if self.agent_config.import_agents(args.input) else 1
    
    def cmd_info(self, args) -> int:
        """Show agent information"""
        config = self.agent_config.load_agent(args.name)
        if not config:
            return 1
        
        print()
        print(json.dumps(config, indent=2))
        print()
        return 0
    
    def cmd_docs(self, args) -> int:
        """Generate documentation"""
        doc = self.agent_config.generate_documentation(args.name)
        if not doc:
            return 1
        
        print(doc)
        return 0

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Agent Configuration Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Initialize new agent
  python3 agent_config.py init my-agent
  
  # List all agents
  python3 agent_config.py list
  
  # Create agent with options
  python3 agent_config.py create my-agent --type worker --description "Worker agent"
  
  # Validate configuration
  python3 agent_config.py validate my-agent
  
  # Export configurations
  python3 agent_config.py export --output agents.json
  
  # Generate documentation
  python3 agent_config.py docs my-agent
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # init command
    init_parser = subparsers.add_parser('init', help='Initialize new agent')
    init_parser.add_argument('name', help='Agent name')
    init_parser.set_defaults(func=AgentConfigCLI().cmd_init)
    
    # list command
    list_parser = subparsers.add_parser('list', help='List all agents')
    list_parser.set_defaults(func=AgentConfigCLI().cmd_list)
    
    # create command
    create_parser = subparsers.add_parser('create', help='Create agent')
    create_parser.add_argument('name', help='Agent name')
    create_parser.add_argument('--type', help='Agent type')
    create_parser.add_argument('--description', help='Agent description')
    create_parser.set_defaults(func=AgentConfigCLI().cmd_create)
    
    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate agent')
    validate_parser.add_argument('name', help='Agent name')
    validate_parser.set_defaults(func=AgentConfigCLI().cmd_validate)
    
    # export command
    export_parser = subparsers.add_parser('export', help='Export configurations')
    export_parser.add_argument('--output', help='Output file')
    export_parser.set_defaults(func=AgentConfigCLI().cmd_export)
    
    # import command
    import_parser = subparsers.add_parser('import', help='Import configurations')
    import_parser.add_argument('input', help='Input file')
    import_parser.set_defaults(func=AgentConfigCLI().cmd_import)
    
    # info command
    info_parser = subparsers.add_parser('info', help='Show agent info')
    info_parser.add_argument('name', help='Agent name')
    info_parser.set_defaults(func=AgentConfigCLI().cmd_info)
    
    # docs command
    docs_parser = subparsers.add_parser('docs', help='Generate documentation')
    docs_parser.add_argument('name', help='Agent name')
    docs_parser.set_defaults(func=AgentConfigCLI().cmd_docs)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Call command handler
    if hasattr(args, 'func'):
        sys.exit(args.func(args))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
