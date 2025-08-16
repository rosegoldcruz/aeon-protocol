"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Loader2, Film, Play, Settings, Sparkles, Video, Scissors, Wand2, Camera, Mic } from "lucide-react"


interface LibraryItem {
  id: string
  prompt: string
  createdAt: number
  url: string
  duration: number
  resolution: string
}

interface VideoHubProps {
  isGenerating: boolean
}

export function VideoHub({ isGenerating }: VideoHubProps) {
  const [prompt, setPrompt] = useState("")
  const [provider, setProvider] = useState("replicate-hailuo")
  const [duration, setDuration] = useState([6])
  const [resolution, setResolution] = useState("768p")
  const [fps, setFps] = useState([24])
  const [seed, setSeed] = useState("")

  const [predictionId, setPredictionId] = useState<string | null>(null)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [status, setStatus] = useState<string | null>(null) // used in UI texts
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const playerRef = useRef<HTMLVideoElement | null>(null)

  const LIB_KEY = "aeon_video_library_v1"
  const library: LibraryItem[] = useMemo(() => {
    if (typeof window === "undefined") return []
    try { return JSON.parse(localStorage.getItem(LIB_KEY) || "[]") } catch { return [] }
  }, [])
  const [items, setItems] = useState<LibraryItem[]>(library)

  const saveToLibrary = (item: LibraryItem) => {
    const next = [item, ...items].slice(0, 100)
    setItems(next)
    if (typeof window !== "undefined") localStorage.setItem(LIB_KEY, JSON.stringify(next))
  }

  const handleGenerate = async () => {
    setError(null)
    setVideoUrl(null)
    setStatus("starting")
    setLoading(true)

    try {
      const resp = await fetch("/api/video/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim(), duration: duration[0], resolution }),
      })
      const data = await resp.json()
      if (!resp.ok) {
        setStatus("failed")
        setError(data?.error || "Failed to start prediction")
        setLoading(false)
        return
      }
      setPredictionId(data.id)
    } catch (e) {
      console.error(e)
      setStatus("failed")
      setError("Network error occurred")
      setLoading(false)
    }
  }

  // Polling for status
  useEffect(() => {
    if (!predictionId) return
    let mounted = true
    const interval = setInterval(async () => {
      try {
        const resp = await fetch(`/api/video/status?id=${predictionId}`, { cache: "no-store" })
        const data = await resp.json()
        if (!resp.ok) throw new Error(data?.error || "status error")
        if (!mounted) return
        setStatus(data.status)

        if (data.error) setError(data.error)

        if (data.status === "succeeded" && data.output) {
          setVideoUrl(data.output as string)
          setLoading(false)
          clearInterval(interval)
          const item: LibraryItem = {
            id: predictionId,
            prompt: prompt.trim(),
            createdAt: Date.now(),
            url: data.output as string,
            duration: duration[0] ?? 6,
            resolution,
          }
          saveToLibrary(item)
        }
        if (["failed", "canceled"].includes(data.status)) {
          setLoading(false)
          clearInterval(interval)
        }
      } catch (e) {
        console.error(e)
        setLoading(false)
        clearInterval(interval)
      }
    }, 2000)

    return () => { mounted = false; clearInterval(interval) }
  }, [predictionId])

  const providers = [
    { id: "runway", name: "Runway Gen-3", description: "High-quality cinematic videos" },
    { id: "pika", name: "Pika Labs", description: "Creative and artistic videos" },
    { id: "luma", name: "Luma Dream Machine", description: "Realistic motion and physics" },
    { id: "hailuo", name: "Hailuo AI", description: "Fast generation with good quality" }
  ]

  const resolutions = [
    { value: "1280x768", label: "1280x768 (16:10)" },
    { value: "1920x1080", label: "1920x1080 (16:9)" },
    { value: "1024x1024", label: "1024x1024 (1:1)" },
    { value: "768x1280", label: "768x1280 (9:16)" }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500">
          <Film className="h-8 w-8 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Video Hub</h2>
          <p className="text-gray-400">Professional video production and editing</p>
        </div>
      </div>

      <Tabs defaultValue="generate" className="w-full">
        <TabsList className="grid w-full grid-cols-5 bg-gray-800">
          <TabsTrigger value="generate" className="data-[state=active]:bg-gray-700">
            <Wand2 className="h-4 w-4 mr-2" />
            Generate
          </TabsTrigger>
          <TabsTrigger value="edit" className="data-[state=active]:bg-gray-700">
            <Scissors className="h-4 w-4 mr-2" />
            Edit
          </TabsTrigger>
          <TabsTrigger value="enhance" className="data-[state=active]:bg-gray-700">
            <Sparkles className="h-4 w-4 mr-2" />
            Enhance
          </TabsTrigger>
          <TabsTrigger value="convert" className="data-[state=active]:bg-gray-700">
            <Camera className="h-4 w-4 mr-2" />
            Convert
          </TabsTrigger>
          <TabsTrigger value="dub" className="data-[state=active]:bg-gray-700">
            <Mic className="h-4 w-4 mr-2" />
            Dub
          </TabsTrigger>
        </TabsList>

        <TabsContent value="generate" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Generation Controls */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Play className="h-5 w-5" />
                  Video Generation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Prompt */}
                <div className="space-y-2">
                  <Label className="text-white">Video Description</Label>
                  <Input
                    placeholder="A time-lapse of a flower blooming in spring, cinematic lighting, 4K quality..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>

                {/* Provider Selection */}
                <div className="space-y-2">
                  <Label className="text-white">AI Provider</Label>
                  <Select value={provider} onValueChange={setProvider}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      {providers.map((p) => (
                        <SelectItem key={p.id} value={p.id} className="text-white">
                          <div>
                            <div className="font-medium">{p.name}</div>
                            <div className="text-sm text-gray-400">{p.description}</div>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Resolution */}
                <div className="space-y-2">
                  <Label className="text-white">Resolution</Label>
                  <Select value={resolution} onValueChange={setResolution}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      {resolutions.map((res) => (
                        <SelectItem key={res.value} value={res.value} className="text-white">
                          {res.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Duration */}
                <div className="space-y-2">
                  <Label className="text-white">Duration: {duration[0]} seconds</Label>
                  <Slider
                    value={duration}
                    onValueChange={setDuration}
                    max={10}
                    min={2}
                    step={1}
                    className="w-full"
                  />
                </div>

                {/* FPS */}
                <div className="space-y-2">
                  <Label className="text-white">Frame Rate: {fps[0]} FPS</Label>
                  <Slider
                    value={fps}
                    onValueChange={setFps}
                    max={60}
                    min={12}
                    step={12}
                    className="w-full"
                  />
                </div>

                {/* Seed */}
                <div className="space-y-2">
                  <Label className="text-white">Seed (Optional)</Label>
                  <Input
                    placeholder="Random seed for reproducible results"
                    value={seed}
                    onChange={(e) => setSeed(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white"
                    type="number"
                  />
                </div>

                {/* Generate Button */}
                <Button 
                  onClick={handleGenerate} 
                  disabled={isGenerating || !prompt.trim()}
                  className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Generating Video...
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Generate Video
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Preview & Features */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Features & Preview
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="aspect-video bg-black rounded-lg flex items-center justify-center overflow-hidden">
                  {videoUrl ? (
                    <video
                      ref={playerRef}
                      className="w-full h-full"
                      src={videoUrl}
                      controls
                      playsInline
                    />
                  ) : (
                    <div className="text-center text-gray-400">
                      {predictionId ? (
                        <>
                          <Loader2 className="h-8 w-8 mx-auto mb-2 animate-spin" />
                          <p className="text-sm">Status: {status || "starting"}</p>
                        </>
                      ) : (
                        <>
                          <Video className="h-12 w-12 mx-auto mb-2" />
                          <p>Video preview will appear here</p>
                        </>
                      )}
                    </div>
                  )}
                </div>

                {!videoUrl && error && (
                  <p className="text-red-400 text-sm mt-2">Error: {error}</p>
                )}

                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={isGenerating || loading || !prompt.trim()} className="bg-blue-600 hover:bg-blue-700">
                    {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
                    {loading ? "Generating..." : "Generate"}
                  </Button>
                  {videoUrl && (
                    <Button asChild variant="outline" className="border-gray-600 text-white">
                      <a href={videoUrl} download target="_blank" rel="noopener noreferrer">Download</a>
                    </Button>
                  )}
                </div>

                <div className="space-y-2">
                  <h4 className="font-semibold text-white">Your Library</h4>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {items.length === 0 && (
                      <div className="col-span-full text-sm text-gray-400">No videos yet. Generate your first video above.</div>
                    )}
                    {items.map((it) => (
                      <div key={it.id} className="bg-gray-700 rounded p-2 space-y-2">
                        <div className="aspect-video bg-black rounded overflow-hidden">
                          <video src={it.url} className="w-full h-full" controls={false} muted playsInline />
                        </div>
                        <div className="text-xs text-gray-300 truncate" title={it.prompt}>{it.prompt}</div>
                        <div className="flex justify-between text-xs text-gray-400">
                          <span>{new Date(it.createdAt).toLocaleString()}</span>
                          <a href={it.url} download className="text-blue-400 hover:underline">Download</a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="edit" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">✂️</div>
                <h3 className="text-2xl font-semibold text-white">Video Editing</h3>
                <p className="text-gray-400">
                  Advanced video editing tools with AI-powered cuts, transitions, and effects coming soon.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="enhance" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">✨</div>
                <h3 className="text-2xl font-semibold text-white">Video Enhancement</h3>
                <p className="text-gray-400">
                  AI-powered video upscaling, denoising, and quality enhancement tools coming soon.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="convert" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🔄</div>
                <h3 className="text-2xl font-semibold text-white">Image-to-Video</h3>
                <p className="text-gray-400">
                  Convert static images to dynamic videos with motion control and camera movements.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="dub" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🎤</div>
                <h3 className="text-2xl font-semibold text-white">Multi-language Dubbing</h3>
                <p className="text-gray-400">
                  AI-powered voice cloning and lip-sync technology for multi-language dubbing.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}


