"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import {
  Loader2,
  Code,
  Wand2,
  Globe,
  Smartphone,
  Database,
  Settings,
  Eye,
  Zap
} from "lucide-react"

interface AiCoderProps {
  onGenerate: (data: any) => void
  isGenerating: boolean
}

export function AiCoder({ onGenerate, isGenerating }: AiCoderProps) {
  const [description, setDescription] = useState("")
  const [appType, setAppType] = useState("web")
  const [features, setFeatures] = useState("")
  const [style, setStyle] = useState("")

  const handleGenerate = () => {
    onGenerate({
      description: description.trim(),
      app_type: appType,
      features: features.trim(),
      style: style.trim()
    })
  }

  const appTypes = [
    { id: "web", name: "Web App", icon: Globe, description: "React/Next.js web application" },
    { id: "mobile", name: "Mobile App", icon: Smartphone, description: "React Native mobile app" },
    { id: "api", name: "API Service", icon: Database, description: "REST API with database" },
    { id: "dashboard", name: "Dashboard", icon: Settings, description: "Admin/analytics dashboard" }
  ]

  const examples = [
    {
      title: "E-commerce Store",
      description: "Create an online store with product catalog, shopping cart, and payment processing",
      features: "Product listings, cart, checkout, user accounts, order tracking",
      style: "Modern, clean design with blue and white color scheme"
    },
    {
      title: "Task Manager",
      description: "Build a productivity app for managing tasks and projects",
      features: "Task creation, due dates, categories, progress tracking, team collaboration",
      style: "Minimalist design with dark theme and purple accents"
    },
    {
      title: "Blog Platform",
      description: "Create a content management system for blogging",
      features: "Post creation, categories, comments, user profiles, SEO optimization",
      style: "Clean typography-focused design with customizable themes"
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-lg bg-gradient-to-br from-gray-700 to-gray-900">
          <Code className="h-8 w-8 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">AI Coder</h2>
          <p className="text-gray-400">Natural language to web apps - no coding required</p>
        </div>
      </div>

      <Tabs defaultValue="create" className="w-full">
        <TabsList className="grid w-full grid-cols-3 bg-gray-800">
          <TabsTrigger value="create" className="data-[state=active]:bg-gray-700">
            <Wand2 className="h-4 w-4 mr-2" />
            Create App
          </TabsTrigger>
          <TabsTrigger value="examples" className="data-[state=active]:bg-gray-700">
            <Eye className="h-4 w-4 mr-2" />
            Examples
          </TabsTrigger>
          <TabsTrigger value="deploy" className="data-[state=active]:bg-gray-700">
            <Zap className="h-4 w-4 mr-2" />
            Deploy
          </TabsTrigger>
        </TabsList>

        <TabsContent value="create" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* App Creation Form */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Wand2 className="h-5 w-5" />
                  Describe Your App
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Tell us what you want to build in natural language
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* App Description */}
                <div className="space-y-2">
                  <Label className="text-white">What do you want to build?</Label>
                  <Input
                    placeholder="I want to create a social media app where users can share photos and follow each other..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white min-h-[100px]"
                  />
                </div>

                {/* Features */}
                <div className="space-y-2">
                  <Label className="text-white">Key Features (Optional)</Label>
                  <Input
                    placeholder="User authentication, photo upload, likes, comments, following system..."
                    value={features}
                    onChange={(e) => setFeatures(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>

                {/* Style Preferences */}
                <div className="space-y-2">
                  <Label className="text-white">Design Style (Optional)</Label>
                  <Input
                    placeholder="Modern, dark theme, blue accents, mobile-first design..."
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>

                {/* Generate Button */}
                <Button 
                  onClick={handleGenerate} 
                  disabled={isGenerating || !description.trim()}
                  className="w-full bg-gradient-to-r from-gray-700 to-gray-900 hover:from-gray-600 hover:to-gray-800"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Building Your App...
                    </>
                  ) : (
                    <>
                      <Code className="h-4 w-4 mr-2" />
                      Generate App
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* App Type Selection */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white">App Type</CardTitle>
                <CardDescription className="text-gray-400">
                  Choose the type of application you want to create
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  {appTypes.map((type) => (
                    <div
                      key={type.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-all ${
                        appType === type.id
                          ? "border-blue-500 bg-blue-500/10"
                          : "border-gray-600 hover:border-gray-500"
                      }`}
                      onClick={() => setAppType(type.id)}
                    >
                      <type.icon className="h-8 w-8 text-white mb-2" />
                      <h4 className="font-semibold text-white text-sm">{type.name}</h4>
                      <p className="text-xs text-gray-400">{type.description}</p>
                    </div>
                  ))}
                </div>

                <div className="space-y-3 pt-4 border-t border-gray-700">
                  <h4 className="font-semibold text-white">What You'll Get:</h4>
                  <div className="space-y-2 text-sm text-gray-300">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      Complete source code
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      Modern UI components
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      Database integration
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      API endpoints
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      Deployment ready
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="examples" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {examples.map((example, index) => (
              <Card key={index} className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white">{example.title}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-gray-300 text-sm">{example.description}</p>
                  <div className="space-y-2">
                    <p className="text-xs text-gray-400"><strong>Features:</strong> {example.features}</p>
                    <p className="text-xs text-gray-400"><strong>Style:</strong> {example.style}</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setDescription(example.description)
                      setFeatures(example.features)
                      setStyle(example.style)
                    }}
                    className="w-full bg-gray-700 border-gray-600 text-white hover:bg-gray-600"
                  >
                    Use This Example
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="deploy" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🚀</div>
                <h3 className="text-2xl font-semibold text-white">One-Click Deployment</h3>
                <p className="text-gray-400">
                  Deploy your generated apps instantly to Vercel, Netlify, or your own infrastructure.
                </p>
                <div className="flex justify-center gap-4 pt-4">
                  <div className="p-3 bg-gray-700 rounded-lg">
                    <Globe className="h-6 w-6 text-white" />
                  </div>
                  <div className="p-3 bg-gray-700 rounded-lg">
                    <Database className="h-6 w-6 text-white" />
                  </div>
                  <div className="p-3 bg-gray-700 rounded-lg">
                    <Zap className="h-6 w-6 text-white" />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
