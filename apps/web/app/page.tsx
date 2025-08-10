"use client"

import { useState, useEffect } from "react"
import { useAuth, useUser } from "@clerk/nextjs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { AuthHeader } from "@/components/auth/auth-header"
import { apiRequest } from "@/lib/utils"
import { Loader2, Image as ImageIcon, Clock, CheckCircle, XCircle, Video, Music, Bot, Briefcase } from "lucide-react"

interface Job {
  id: number
  type: string
  status: string
  input_data: any
  output_data?: any
  created_at: string
  completed_at?: string
  error_message?: string
}

interface Asset {
  id: number
  s3_key: string
  s3_bucket: string
  media_type: string
  presigned_url?: string
}

export default function HomePage() {
  const { getToken, isLoaded: authLoaded } = useAuth()
  const { user, isLoaded: userLoaded } = useUser()
  const [prompt, setPrompt] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [jobs, setJobs] = useState<Job[]>([])
  const [assets, setAssets] = useState<{ [jobId: number]: Asset[] }>({})
  const [activeTab, setActiveTab] = useState("image")

  const fetchJobs = async () => {
    if (!authLoaded || !userLoaded) return

    try {
      const token = await getToken()
      if (!token) return

      const response = await apiRequest("/v1/jobs", {}, token)
      setJobs(response.jobs || [])
    } catch (error) {
      console.error("Failed to fetch jobs:", error)
    }
  }

  const fetchJobAssets = async (jobId: number) => {
    if (!authLoaded || !userLoaded) return

    try {
      const token = await getToken()
      if (!token) return

      const response = await apiRequest(`/v1/jobs/${jobId}/assets`, {}, token)
      setAssets(prev => ({ ...prev, [jobId]: response }))
    } catch (error) {
      console.error("Failed to fetch assets:", error)
    }
  }

  useEffect(() => {
    if (authLoaded && userLoaded && user) {
      fetchJobs()
      const interval = setInterval(fetchJobs, 3000) // Poll every 3 seconds
      return () => clearInterval(interval)
    }
  }, [authLoaded, userLoaded, user])

  useEffect(() => {
    // Fetch assets for completed jobs
    jobs.forEach(job => {
      if (job.status === "completed" && !assets[job.id]) {
        fetchJobAssets(job.id)
      }
    })
  }, [jobs, assets])

  const handleGenerate = async () => {
    if (!prompt.trim() || !authLoaded || !userLoaded) return

    setIsGenerating(true)
    try {
      const token = await getToken()
      if (!token) {
        console.error("No authentication token available")
        return
      }

      let endpoint = "/v1/jobs/image-generate"
      let payload: any = {
        prompt: prompt.trim(),
        model: "flux-schnell",
        width: 1024,
        height: 1024,
        num_outputs: 1
      }

      if (activeTab === "video") {
        endpoint = "/v1/jobs/video-generate"
        payload = {
          prompt: prompt.trim(),
          provider: "runway",
          duration: 5,
          resolution: "1280x768"
        }
      } else if (activeTab === "audio") {
        endpoint = "/v1/jobs/audio-generate"
        payload = {
          text: prompt.trim(),
          voice_id: "21m00Tcm4TlvDq8ikWAM"
        }
      }

      await apiRequest(endpoint, {
        method: "POST",
        body: JSON.stringify(payload)
      }, token)
      setPrompt("")
      fetchJobs() // Refresh jobs list
    } catch (error) {
      console.error("Failed to generate content:", error)
    } finally {
      setIsGenerating(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "pending":
        return <Clock className="h-4 w-4 text-yellow-500" />
      case "processing":
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
      case "completed":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "failed":
        return <XCircle className="h-4 w-4 text-red-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  if (!authLoaded || !userLoaded) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center min-h-screen">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center min-h-screen">
          <Card className="max-w-md">
            <CardHeader>
              <CardTitle>Welcome to AEON</CardTitle>
              <CardDescription>Please sign in to continue</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <AuthHeader />

      <div className="container mx-auto p-6 space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold">AEON</h1>
          <p className="text-muted-foreground">Unified AI business automation platform</p>
        </div>

      {/* Media Generation Tabs */}
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>AEON Media Studio</CardTitle>
          <CardDescription>
            Generate images, videos, and audio using AI. Choose your media type below.
          </CardDescription>

          {/* Tab Navigation */}
          <div className="flex gap-2 mt-4">
            <Button
              variant={activeTab === "image" ? "default" : "outline"}
              onClick={() => setActiveTab("image")}
              className="flex items-center gap-2"
            >
              <ImageIcon className="h-4 w-4" />
              Images
            </Button>
            <Button
              variant={activeTab === "video" ? "default" : "outline"}
              onClick={() => setActiveTab("video")}
              className="flex items-center gap-2"
            >
              <Video className="h-4 w-4" />
              Videos
            </Button>
            <Button
              variant={activeTab === "audio" ? "default" : "outline"}
              onClick={() => setActiveTab("audio")}
              className="flex items-center gap-2"
            >
              <Music className="h-4 w-4" />
              Audio
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Dynamic Content Based on Tab */}
          {activeTab === "image" && (
            <div className="space-y-2">
              <h3 className="font-semibold">Image Generation</h3>
              <p className="text-sm text-muted-foreground">
                Create stunning images from text descriptions using FLUX and other advanced models.
              </p>
            </div>
          )}

          {activeTab === "video" && (
            <div className="space-y-2">
              <h3 className="font-semibold">Video Production</h3>
              <p className="text-sm text-muted-foreground">
                Generate videos from text prompts using Runway, Pika, Luma, and Hailuo AI.
              </p>
            </div>
          )}

          {activeTab === "audio" && (
            <div className="space-y-2">
              <h3 className="font-semibold">Audio Generation</h3>
              <p className="text-sm text-muted-foreground">
                Create realistic speech and audio using ElevenLabs voice synthesis.
              </p>
            </div>
          )}

          {/* Generation Form */}
          <div className="flex gap-2">
            <Input
              placeholder={
                activeTab === "image"
                  ? "A futuristic city at sunset with flying cars..."
                  : activeTab === "video"
                  ? "A time-lapse of a flower blooming in spring..."
                  : "Hello, welcome to AEON. This is a test of our voice synthesis."
              }
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
              disabled={isGenerating}
            />
            <Button onClick={handleGenerate} disabled={isGenerating || !prompt.trim()}>
              {isGenerating ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                `Generate ${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}`
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* AI Agents Section */}
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            AI Agent Ecosystem
          </CardTitle>
          <CardDescription>
            Intelligent agents for content creation and business automation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 border rounded-lg text-center">
              <Bot className="h-8 w-8 mx-auto mb-2 text-blue-500" />
              <h4 className="font-semibold text-sm">Screenwriter</h4>
              <p className="text-xs text-muted-foreground">Script generation & story analysis</p>
            </div>
            <div className="p-4 border rounded-lg text-center">
              <Video className="h-8 w-8 mx-auto mb-2 text-green-500" />
              <h4 className="font-semibold text-sm">Video Editor</h4>
              <p className="text-xs text-muted-foreground">Automated editing & pacing</p>
            </div>
            <div className="p-4 border rounded-lg text-center">
              <Briefcase className="h-8 w-8 mx-auto mb-2 text-purple-500" />
              <h4 className="font-semibold text-sm">Sales Agent</h4>
              <p className="text-xs text-muted-foreground">Lead qualification & proposals</p>
            </div>
            <div className="p-4 border rounded-lg text-center">
              <Bot className="h-8 w-8 mx-auto mb-2 text-orange-500" />
              <h4 className="font-semibold text-sm">Marketing</h4>
              <p className="text-xs text-muted-foreground">Campaign creation & optimization</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Jobs List */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Recent Jobs</h2>
        {jobs.length === 0 ? (
          <Card>
            <CardContent className="p-6 text-center text-muted-foreground">
              No jobs yet. Generate your first image above!
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {jobs.map((job) => (
              <Card key={job.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg flex items-center gap-2">
                      {getStatusIcon(job.status)}
                      Job #{job.id}
                    </CardTitle>
                    <span className="text-sm text-muted-foreground capitalize">
                      {job.status}
                    </span>
                  </div>
                  <CardDescription>
                    {job.input_data?.prompt || "No prompt"}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="text-sm text-muted-foreground">
                      Created: {new Date(job.created_at).toLocaleString()}
                      {job.completed_at && (
                        <> • Completed: {new Date(job.completed_at).toLocaleString()}</>
                      )}
                    </div>

                    {job.error_message && (
                      <div className="text-sm text-red-500 bg-red-50 p-2 rounded">
                        Error: {job.error_message}
                      </div>
                    )}

                    {job.status === "completed" && assets[job.id] && (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {assets[job.id].map((asset) => (
                          <div key={asset.id} className="space-y-2">
                            {asset.presigned_url ? (
                              asset.media_type === "image" ? (
                                <img
                                  src={asset.presigned_url}
                                  alt="Generated image"
                                  className="w-full h-48 object-cover rounded-lg border"
                                />
                              ) : asset.media_type === "video" ? (
                                <video
                                  src={asset.presigned_url}
                                  controls
                                  className="w-full h-48 object-cover rounded-lg border"
                                />
                              ) : asset.media_type === "audio" ? (
                                <div className="w-full p-4 bg-muted rounded-lg border">
                                  <audio src={asset.presigned_url} controls className="w-full" />
                                </div>
                              ) : (
                                <div className="w-full h-48 bg-muted rounded-lg border flex items-center justify-center">
                                  <p className="text-sm">Unknown media type</p>
                                </div>
                              )
                            ) : (
                              <div className="w-full h-48 bg-muted rounded-lg border flex items-center justify-center">
                                <Loader2 className="h-6 w-6 animate-spin" />
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
    </div>
  )
}

