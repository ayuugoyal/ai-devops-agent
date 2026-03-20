"""
MCP Server Registry
Single source of truth for all known official MCP servers.
Used by the setup wizard and the proxy manager at runtime.

Sources:
  AWS  → https://github.com/awslabs/mcp  (67+ official servers)
  Others → official MCP community servers
"""

# Each entry schema:
# {
#   "id":          str   — unique key used in config.json
#   "name":        str   — human label shown in setup wizard
#   "description": str   — one-line description
#   "package":     str   — PyPI package name (for uvx / pip)
#   "command":     str   — executable to launch ("uvx" | "npx" | "python")
#   "args":        list  — args passed to command
#   "env_vars": {
#       KEY: {
#           "required": bool,
#           "secret":   bool,   # stored in keyring, never in config.json
#           "label":    str,    # shown in setup wizard
#           "default":  str,    # optional default value
#       }
#   },
#   "tools_preview": list[str]  — sample tool names shown in wizard
# }

MCP_REGISTRY: dict = {

    # ── AWS ──────────────────────────────────────────────────────────────────

    "aws": {
        "label": "Amazon Web Services",
        "icon": "☁️",
        "servers": {

            "awslabs.cost-explorer": {
                "id": "awslabs.cost-explorer",
                "name": "AWS Cost Explorer",
                "description": "Query cost & usage, forecasts, and savings plan recommendations",
                "package": "awslabs.cost-explorer-mcp-server",
                "command": "uvx",
                "args": ["awslabs.cost-explorer-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True,  "secret": True,  "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True,  "secret": True,  "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["get_cost_and_usage", "get_cost_forecast", "get_savings_plan_recommendations"],
            },

            "awslabs.billing-cost-management": {
                "id": "awslabs.billing-cost-management",
                "name": "AWS Billing & Cost Management",
                "description": "Bills, invoices, free-tier usage, and budget alerts",
                "package": "awslabs.billing-cost-management-mcp-server",
                "command": "uvx",
                "args": ["awslabs.billing-cost-management-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True,  "secret": True,  "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True,  "secret": True,  "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_bills", "get_invoice", "get_free_tier_usage"],
            },

            "awslabs.aws-pricing": {
                "id": "awslabs.aws-pricing",
                "name": "AWS Pricing",
                "description": "Look up on-demand and spot pricing for any AWS service",
                "package": "awslabs.aws-pricing-mcp-server",
                "command": "uvx",
                "args": ["awslabs.aws-pricing-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True,  "secret": True,  "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True,  "secret": True,  "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["get_ec2_pricing", "get_rds_pricing", "list_services"],
            },

            "awslabs.cloudwatch": {
                "id": "awslabs.cloudwatch",
                "name": "AWS CloudWatch",
                "description": "Metrics, alarms, dashboards, and log insights",
                "package": "awslabs.cloudwatch-mcp-server",
                "command": "uvx",
                "args": ["awslabs.cloudwatch-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True,  "secret": True,  "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True,  "secret": True,  "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["get_metric_data", "list_alarms", "put_metric_alarm", "query_logs_insights"],
            },

            "awslabs.cloudwatch-applicationsignals": {
                "id": "awslabs.cloudwatch-applicationsignals",
                "name": "AWS CloudWatch Application Signals",
                "description": "APM signals, SLOs, and service health",
                "package": "awslabs.cloudwatch-applicationsignals-mcp-server",
                "command": "uvx",
                "args": ["awslabs.cloudwatch-applicationsignals-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_services", "get_service_slos", "get_service_health"],
            },

            "awslabs.cloudtrail": {
                "id": "awslabs.cloudtrail",
                "name": "AWS CloudTrail",
                "description": "API audit logs, event history, and compliance",
                "package": "awslabs.cloudtrail-mcp-server",
                "command": "uvx",
                "args": ["awslabs.cloudtrail-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["lookup_events", "get_trail_status", "list_trails"],
            },

            "awslabs.ecs": {
                "id": "awslabs.ecs",
                "name": "Amazon ECS",
                "description": "ECS clusters, services, tasks, and container deployments",
                "package": "awslabs.ecs-mcp-server",
                "command": "uvx",
                "args": ["awslabs.ecs-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_clusters", "list_services", "update_service", "run_task", "get_task_logs"],
            },

            "awslabs.eks": {
                "id": "awslabs.eks",
                "name": "Amazon EKS",
                "description": "EKS clusters, node groups, and Kubernetes workloads",
                "package": "awslabs.eks-mcp-server",
                "command": "uvx",
                "args": ["awslabs.eks-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_clusters", "describe_cluster", "list_nodegroups", "get_kubeconfig"],
            },

            "awslabs.lambda-tool": {
                "id": "awslabs.lambda-tool",
                "name": "AWS Lambda",
                "description": "Invoke, deploy, and manage Lambda functions",
                "package": "awslabs.lambda-tool-mcp-server",
                "command": "uvx",
                "args": ["awslabs.lambda-tool-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["invoke_function", "list_functions", "update_function_code", "get_function_logs"],
            },

            "awslabs.sagemaker-ai": {
                "id": "awslabs.sagemaker-ai",
                "name": "Amazon SageMaker",
                "description": "ML training jobs, endpoints, models, and notebooks",
                "package": "awslabs.sagemaker-ai-mcp-server",
                "command": "uvx",
                "args": ["awslabs.sagemaker-ai-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_training_jobs", "describe_endpoint", "invoke_endpoint", "list_models"],
            },

            "awslabs.dynamodb": {
                "id": "awslabs.dynamodb",
                "name": "Amazon DynamoDB",
                "description": "DynamoDB tables, queries, scans, and item operations",
                "package": "awslabs.dynamodb-mcp-server",
                "command": "uvx",
                "args": ["awslabs.dynamodb-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_tables", "query", "scan", "put_item", "delete_item"],
            },

            "awslabs.redshift": {
                "id": "awslabs.redshift",
                "name": "Amazon Redshift",
                "description": "Redshift clusters, query execution, and data warehouse operations",
                "package": "awslabs.redshift-mcp-server",
                "command": "uvx",
                "args": ["awslabs.redshift-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["execute_query", "list_clusters", "describe_table", "get_query_results"],
            },

            "awslabs.elasticache": {
                "id": "awslabs.elasticache",
                "name": "Amazon ElastiCache",
                "description": "Redis/Memcached clusters, replication groups, and cache operations",
                "package": "awslabs.elasticache-mcp-server",
                "command": "uvx",
                "args": ["awslabs.elasticache-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_clusters", "describe_replication_group", "failover_primary"],
            },

            "awslabs.documentdb": {
                "id": "awslabs.documentdb",
                "name": "Amazon DocumentDB",
                "description": "DocumentDB cluster and instance management",
                "package": "awslabs.documentdb-mcp-server",
                "command": "uvx",
                "args": ["awslabs.documentdb-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_clusters", "describe_cluster", "list_instances"],
            },

            "awslabs.aurora-dsql": {
                "id": "awslabs.aurora-dsql",
                "name": "Aurora DSQL",
                "description": "Aurora DSQL distributed SQL cluster operations",
                "package": "awslabs.aurora-dsql-mcp-server",
                "command": "uvx",
                "args": ["awslabs.aurora-dsql-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_clusters", "create_cluster", "execute_statement"],
            },

            "awslabs.iam": {
                "id": "awslabs.iam",
                "name": "AWS IAM",
                "description": "Roles, policies, users, groups, and permission analysis",
                "package": "awslabs.iam-mcp-server",
                "command": "uvx",
                "args": ["awslabs.iam-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_roles", "list_policies", "simulate_policy", "get_role"],
            },

            "awslabs.aws-network": {
                "id": "awslabs.aws-network",
                "name": "AWS Networking",
                "description": "VPCs, subnets, security groups, route tables, and NACLs",
                "package": "awslabs.aws-network-mcp-server",
                "command": "uvx",
                "args": ["awslabs.aws-network-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_vpcs", "list_security_groups", "describe_route_table"],
            },

            "awslabs.amazon-sns-sqs": {
                "id": "awslabs.amazon-sns-sqs",
                "name": "Amazon SNS & SQS",
                "description": "Topics, queues, publish, subscribe, and message management",
                "package": "awslabs.amazon-sns-sqs-mcp-server",
                "command": "uvx",
                "args": ["awslabs.amazon-sns-sqs-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_topics", "publish_message", "send_message", "receive_messages", "list_queues"],
            },

            "awslabs.cdk": {
                "id": "awslabs.cdk",
                "name": "AWS CDK",
                "description": "Generate and deploy CDK infrastructure-as-code",
                "package": "awslabs.cdk-mcp-server",
                "command": "uvx",
                "args": ["awslabs.cdk-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["synth_app", "deploy_stack", "diff_stack", "list_stacks"],
            },

            "awslabs.cfn": {
                "id": "awslabs.cfn",
                "name": "AWS CloudFormation",
                "description": "CloudFormation stacks, change sets, and drift detection",
                "package": "awslabs.cfn-mcp-server",
                "command": "uvx",
                "args": ["awslabs.cfn-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_stacks", "describe_stack", "create_change_set", "detect_stack_drift"],
            },

            "awslabs.terraform": {
                "id": "awslabs.terraform",
                "name": "Terraform (AWS)",
                "description": "Terraform plan, apply, and state management for AWS",
                "package": "awslabs.terraform-mcp-server",
                "command": "uvx",
                "args": ["awslabs.terraform-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["terraform_plan", "terraform_apply", "terraform_state_list"],
            },

            "awslabs.stepfunctions": {
                "id": "awslabs.stepfunctions",
                "name": "AWS Step Functions",
                "description": "State machine definitions, executions, and monitoring",
                "package": "awslabs.stepfunctions-tool-mcp-server",
                "command": "uvx",
                "args": ["awslabs.stepfunctions-tool-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                },
                "tools_preview": ["list_state_machines", "start_execution", "describe_execution"],
            },

            "awslabs.bedrock-kb": {
                "id": "awslabs.bedrock-kb",
                "name": "Amazon Bedrock Knowledge Base",
                "description": "Retrieve from Bedrock Knowledge Bases using RAG",
                "package": "awslabs.bedrock-kb-retrieval-mcp-server",
                "command": "uvx",
                "args": ["awslabs.bedrock-kb-retrieval-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":     {"required": True, "secret": True, "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY": {"required": True, "secret": True, "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":    {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                    "KNOWLEDGE_BASE_ID":     {"required": True, "secret": False, "label": "Bedrock Knowledge Base ID"},
                },
                "tools_preview": ["retrieve", "retrieve_and_generate"],
            },

            "awslabs.aws-documentation": {
                "id": "awslabs.aws-documentation",
                "name": "AWS Documentation",
                "description": "Search and retrieve official AWS documentation",
                "package": "awslabs.aws-documentation-mcp-server",
                "command": "uvx",
                "args": ["awslabs.aws-documentation-mcp-server@latest"],
                "env_vars": {},
                "tools_preview": ["search_docs", "get_doc_page", "recommend"],
            },

            "awslabs.prometheus": {
                "id": "awslabs.prometheus",
                "name": "Amazon Managed Prometheus",
                "description": "Query Prometheus metrics from AWS Managed Prometheus workspaces",
                "package": "awslabs.prometheus-mcp-server",
                "command": "uvx",
                "args": ["awslabs.prometheus-mcp-server@latest"],
                "env_vars": {
                    "AWS_ACCESS_KEY_ID":      {"required": True,  "secret": True,  "label": "AWS Access Key ID"},
                    "AWS_SECRET_ACCESS_KEY":  {"required": True,  "secret": True,  "label": "AWS Secret Access Key"},
                    "AWS_DEFAULT_REGION":     {"required": False, "secret": False, "label": "AWS Region", "default": "us-east-1"},
                    "PROMETHEUS_WORKSPACE_ID":{"required": True,  "secret": False, "label": "Prometheus Workspace ID"},
                },
                "tools_preview": ["query", "query_range", "list_metrics"],
            },
        },
    },

    # ── GRAFANA ───────────────────────────────────────────────────────────────

    "grafana": {
        "label": "Grafana",
        "icon": "📊",
        "servers": {
            "grafana": {
                "id": "grafana",
                "name": "Grafana",
                "description": "Dashboards, datasource queries, alerts, and annotations",
                "package": "mcp-server-grafana",
                "command": "uvx",
                "args": ["mcp-server-grafana"],
                "env_vars": {
                    "GRAFANA_URL":     {"required": True, "secret": False, "label": "Grafana base URL (e.g. https://grafana.mycompany.com)"},
                    "GRAFANA_API_KEY": {"required": True, "secret": True,  "label": "Service Account Token"},
                },
                "tools_preview": ["list_dashboards", "get_dashboard", "query_datasource", "list_alerts", "create_annotation"],
            },
        },
    },

    # ── GITHUB ────────────────────────────────────────────────────────────────

    "github": {
        "label": "GitHub",
        "icon": "🐙",
        "servers": {
            "github": {
                "id": "github",
                "name": "GitHub",
                "description": "Repos, PRs, issues, Actions workflows, and code search",
                "package": "@modelcontextprotocol/server-github",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env_vars": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": {"required": True, "secret": True, "label": "GitHub Personal Access Token"},
                },
                "tools_preview": ["list_repos", "create_pull_request", "list_issues", "get_workflow_runs", "search_code"],
            },
        },
    },

    # ── KUBERNETES ────────────────────────────────────────────────────────────

    "kubernetes": {
        "label": "Kubernetes",
        "icon": "☸️",
        "servers": {
            "kubernetes": {
                "id": "kubernetes",
                "name": "Kubernetes",
                "description": "Pods, deployments, services, logs, and manifest apply",
                "package": "mcp-server-kubernetes",
                "command": "npx",
                "args": ["-y", "mcp-server-kubernetes"],
                "env_vars": {
                    "KUBECONFIG": {"required": False, "secret": False, "label": "kubeconfig path", "default": "~/.kube/config"},
                },
                "tools_preview": ["list_pods", "get_pod_logs", "apply_manifest", "delete_resource", "scale_deployment"],
            },
        },
    },

    # ── PAGERDUTY ─────────────────────────────────────────────────────────────

    "pagerduty": {
        "label": "PagerDuty",
        "icon": "🚨",
        "servers": {
            "pagerduty": {
                "id": "pagerduty",
                "name": "PagerDuty",
                "description": "Incidents, escalations, on-call schedules, and services",
                "package": "mcp-server-pagerduty",
                "command": "uvx",
                "args": ["mcp-server-pagerduty"],
                "env_vars": {
                    "PAGERDUTY_API_KEY": {"required": True, "secret": True, "label": "PagerDuty REST API Key"},
                },
                "tools_preview": ["list_incidents", "acknowledge_incident", "resolve_incident", "get_oncall", "trigger_incident"],
            },
        },
    },

    # ── DATADOG ───────────────────────────────────────────────────────────────

    "datadog": {
        "label": "Datadog",
        "icon": "🐕",
        "servers": {
            "datadog": {
                "id": "datadog",
                "name": "Datadog",
                "description": "Metrics, monitors, logs, APM traces, and dashboards",
                "package": "mcp-server-datadog",
                "command": "uvx",
                "args": ["mcp-server-datadog"],
                "env_vars": {
                    "DD_API_KEY": {"required": True,  "secret": True,  "label": "Datadog API Key"},
                    "DD_APP_KEY": {"required": True,  "secret": True,  "label": "Datadog Application Key"},
                    "DD_SITE":    {"required": False, "secret": False, "label": "Datadog Site", "default": "datadoghq.com"},
                },
                "tools_preview": ["query_metrics", "list_monitors", "get_logs", "mute_monitor", "list_dashboards"],
            },
        },
    },

}


def get_provider_list() -> list[dict]:
    """Return list of {id, label, icon, server_count} for the setup wizard."""
    return [
        {
            "id": k,
            "label": v["label"],
            "icon": v.get("icon", ""),
            "server_count": len(v["servers"]),
        }
        for k, v in MCP_REGISTRY.items()
    ]


def get_servers_for_provider(provider_id: str) -> list[dict]:
    """Return list of server dicts for a given provider."""
    provider = MCP_REGISTRY.get(provider_id, {})
    return list(provider.get("servers", {}).values())


def get_server(server_id: str) -> dict | None:
    """Look up a server by its id across all providers."""
    for provider in MCP_REGISTRY.values():
        server = provider["servers"].get(server_id)
        if server:
            return server
    return None
