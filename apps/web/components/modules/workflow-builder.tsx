"use client"

import { useState, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import {
  Loader2,
  Workflow,
  Play,
  Plus,
  Trash2,
  ArrowRight,
  Settings,
  Zap,
  Video,
  FileText,
  BarChart3,
  Users,
  MessageSquare,
  ShoppingCart
} from "lucide-react"

interface WorkflowStep {
  id: string
  agent_type: string
  name: string
  description: string
  input_mapping: Record<string, string>
  parameters: Record<string, any>
  condition?: string
}

interface WorkflowBuilderProps {
  onSave: (workflow: any) => void
  onExecute: (workflow: any, input: any) => void
  isExecuting: boolean
}

const AVAILABLE_AGENTS = [
  {
    type: "screenwriter",
    name: "Screenwriter Agent",
    description: "Generate scripts with scene breakdown",
    icon: FileText,
    color: "text-blue-500"
  },
  {
    type: "video_editor", 
    name: "Video Editor Agent",
    description: "Multi-scene video generation and stitching",
    icon: Video,
    color: "text-purple-500"
  },
  {
    type: "content_optimizer",
    name: "Content Optimizer",
    description: "Performance prediction and A/B testing",
    icon: BarChart3,
    color: "text-green-500"
  },
  {
    type: "seo_content",
    name: "SEO Content Agent",
    description: "SEO-optimized content generation",
    icon: FileText,
    color: "text-orange-500"
  },
  {
    type: "sales",
    name: "Sales Agent",
    description: "Lead qualification and proposals",
    icon: ShoppingCart,
    color: "text-red-500"
  },
  {
    type: "customer_service",
    name: "Customer Service Agent", 
    description: "Support automation and ticket routing",
    icon: MessageSquare,
    color: "text-cyan-500"
  },
  {
    type: "marketing",
    name: "Marketing Agent",
    description: "Campaign creation and optimization",
    icon: Users,
    color: "text-pink-500"
  },
  {
    type: "analytics",
    name: "Analytics Agent",
    description: "Data analysis and insights",
    icon: BarChart3,
    color: "text-indigo-500"
  }
]

const PREDEFINED_WORKFLOWS = [
  {
    id: "multi_scene_video_production",
    name: "Multi-Scene Video Production",
    description: "Revolutionary workflow: Screenwriter → Video Editor → Content Optimizer",
    agents: ["screenwriter", "video_editor", "content_optimizer"],
    icon: Video,
    revolutionary: true
  },
  {
    id: "content_marketing_campaign",
    name: "Content Marketing Campaign",
    description: "Complete marketing campaign with content and analytics",
    agents: ["marketing", "seo_content", "analytics"],
    icon: Users
  },
  {
    id: "sales_automation_pipeline",
    name: "Sales Automation Pipeline", 
    description: "Automated lead qualification and proposal generation",
    agents: ["sales", "sales", "customer_service"],
    icon: ShoppingCart
  }
]

export function WorkflowBuilder({ onSave, onExecute, isExecuting }: WorkflowBuilderProps) {
  const [workflowName, setWorkflowName] = useState("")
  const [workflowDescription, setWorkflowDescription] = useState("")
  const [steps, setSteps] = useState<WorkflowStep[]>([])
  const [selectedAgent, setSelectedAgent] = useState("")
  const [executionInput, setExecutionInput] = useState("")
  const [activeTab, setActiveTab] = useState("builder")

  const addStep = useCallback(() => {
    if (!selectedAgent) return

    const agent = AVAILABLE_AGENTS.find(a => a.type === selectedAgent)
    if (!agent) return

    const newStep: WorkflowStep = {
      id: `step_${Date.now()}`,
      agent_type: selectedAgent,
      name: agent.name,
      description: agent.description,
      input_mapping: {},
      parameters: {}
    }

    setSteps(prev => [...prev, newStep])
    setSelectedAgent("")
  }, [selectedAgent])

  const removeStep = useCallback((stepId: string) => {
    setSteps(prev => prev.filter(step => step.id !== stepId))
  }, [])

  const updateStep = useCallback((stepId: string, updates: Partial<WorkflowStep>) => {
    setSteps(prev => prev.map(step => 
      step.id === stepId ? { ...step, ...updates } : step
    ))
  }, [])

  const handleSave = useCallback(() => {
    const workflow = {
      name: workflowName,
      description: workflowDescription,
      definition: {
        workflow_type: "custom",
        agents: steps.map(step => step.agent_type),
        steps: steps,
        input_mappings: steps.map(step => step.input_mapping)
      },
      is_active: true
    }
    onSave(workflow)
  }, [workflowName, workflowDescription, steps, onSave])

  const handleExecute = useCallback(() => {
    try {
      const input = executionInput ? JSON.parse(executionInput) : {}
      const workflow = {
        name: workflowName,
        steps: steps
      }
      onExecute(workflow, input)
    } catch (e) {
      alert("Invalid JSON in execution input")
    }
  }, [workflowName, steps, executionInput, onExecute])

  const loadPredefinedWorkflow = useCallback((workflowId: string) => {
    const predefined = PREDEFINED_WORKFLOWS.find(w => w.id === workflowId)
    if (!predefined) return

    setWorkflowName(predefined.name)
    setWorkflowDescription(predefined.description)
    
    const workflowSteps = predefined.agents.map((agentType, index) => {
      const agent = AVAILABLE_AGENTS.find(a => a.type === agentType)
      return {
        id: `step_${index}`,
        agent_type: agentType,
        name: agent?.name || agentType,
        description: agent?.description || "",
        input_mapping: index === 0 ? {} : { "*": "*" }, // First step takes raw input, others take previous output
        parameters: {}
      }
    })
    
    setSteps(workflowSteps)
    setActiveTab("builder")
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-lg bg-gradient-to-br from-purple-700 to-purple-900">
          <Workflow className="h-8 w-8 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Workflow Builder</h2>
          <p className="text-gray-400">Create powerful AI agent workflows with drag-and-drop simplicity</p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="builder">Builder</TabsTrigger>
          <TabsTrigger value="execute">Execute</TabsTrigger>
        </TabsList>

        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Predefined Workflows</CardTitle>
              <CardDescription>Start with proven workflow templates</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {PREDEFINED_WORKFLOWS.map((workflow) => {
                const Icon = workflow.icon
                return (
                  <div
                    key={workflow.id}
                    className={`p-4 border rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors ${
                      workflow.revolutionary ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : ''
                    }`}
                    onClick={() => loadPredefinedWorkflow(workflow.id)}
                  >
                    <div className="flex items-start gap-3">
                      <Icon className={`h-6 w-6 mt-1 ${workflow.revolutionary ? 'text-purple-500' : 'text-gray-500'}`} />
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold">{workflow.name}</h3>
                          {workflow.revolutionary && (
                            <span className="px-2 py-1 text-xs bg-purple-500 text-white rounded-full">
                              Revolutionary
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                          {workflow.description}
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <span className="text-xs text-gray-500">Agents:</span>
                          {workflow.agents.map((agent, index) => (
                            <span key={index} className="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                              {agent}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="builder" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Workflow Configuration</CardTitle>
              <CardDescription>Configure your workflow details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="workflow-name">Workflow Name</Label>
                  <Input
                    id="workflow-name"
                    value={workflowName}
                    onChange={(e) => setWorkflowName(e.target.value)}
                    placeholder="My Custom Workflow"
                  />
                </div>
                <div>
                  <Label htmlFor="workflow-description">Description</Label>
                  <Input
                    id="workflow-description"
                    value={workflowDescription}
                    onChange={(e) => setWorkflowDescription(e.target.value)}
                    placeholder="Workflow description"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Add Agent Step</CardTitle>
              <CardDescription>Select an AI agent to add to your workflow</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Select value={selectedAgent} onValueChange={setSelectedAgent}>
                  <SelectTrigger className="flex-1">
                    <SelectValue placeholder="Select an agent" />
                  </SelectTrigger>
                  <SelectContent>
                    {AVAILABLE_AGENTS.map((agent) => {
                      const Icon = agent.icon
                      return (
                        <SelectItem key={agent.type} value={agent.type}>
                          <div className="flex items-center gap-2">
                            <Icon className={`h-4 w-4 ${agent.color}`} />
                            <span>{agent.name}</span>
                          </div>
                        </SelectItem>
                      )
                    })}
                  </SelectContent>
                </Select>
                <Button onClick={addStep} disabled={!selectedAgent}>
                  <Plus className="h-4 w-4 mr-2" />
                  Add Step
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Workflow Steps ({steps.length})</CardTitle>
              <CardDescription>Configure the sequence of AI agents</CardDescription>
            </CardHeader>
            <CardContent>
              {steps.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  No steps added yet. Select an agent above to get started.
                </div>
              ) : (
                <div className="space-y-4">
                  {steps.map((step, index) => {
                    const agent = AVAILABLE_AGENTS.find(a => a.type === step.agent_type)
                    const Icon = agent?.icon || Settings
                    
                    return (
                      <div key={step.id} className="flex items-center gap-4 p-4 border rounded-lg">
                        <div className="flex items-center gap-3 flex-1">
                          <div className="flex items-center gap-2">
                            <span className="w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm">
                              {index + 1}
                            </span>
                            <Icon className={`h-5 w-5 ${agent?.color || 'text-gray-500'}`} />
                          </div>
                          <div>
                            <h4 className="font-medium">{step.name}</h4>
                            <p className="text-sm text-gray-600 dark:text-gray-400">{step.description}</p>
                          </div>
                        </div>
                        {index < steps.length - 1 && (
                          <ArrowRight className="h-4 w-4 text-gray-400" />
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeStep(step.id)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    )
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          <div className="flex gap-2">
            <Button onClick={handleSave} disabled={!workflowName || steps.length === 0}>
              <Settings className="h-4 w-4 mr-2" />
              Save Workflow
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="execute" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Execute Workflow</CardTitle>
              <CardDescription>Run your workflow with custom input data</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="execution-input">Input Data (JSON)</Label>
                <Textarea
                  id="execution-input"
                  value={executionInput}
                  onChange={(e) => setExecutionInput(e.target.value)}
                  placeholder='{"concept": "A story about AI", "genre": "sci-fi", "target_duration": 120}'
                  rows={6}
                />
              </div>
              
              <Button 
                onClick={handleExecute} 
                disabled={isExecuting || steps.length === 0}
                className="w-full"
              >
                {isExecuting ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Executing Workflow...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Execute Workflow
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
