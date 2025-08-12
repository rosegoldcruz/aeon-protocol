
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Loader2,
  Film,
  Play,
  Settings,
  Sparkles,
  Video,
  Scissors,
  Wand2,
  Camera,
  Mic
} from "lucide-react"

interface VideoHubProps {
  onGenerate: (data: any) => void
  isGenerating: boolean
}

export function VideoHub({ onGenerate, isGenerating }: VideoHubProps) {
  const [prompt, setPrompt] = useState("")
  const [provider, setProvider] = useState("runway")
  const [duration, setDuration] = useState([5])
  const [resolution, setResolution] = useState("1280x768")
  const [fps, setFps] = useState([24])
  const [seed, setSeed] = useState("")

  const handleGenerate = () => {
    onGenerate({
      prompt: prompt.trim(),
      provider,
      duration: duration[0],
      resolution,
      fps: fps[0],
      seed: seed ? parseInt(seed) : undefined
    })
  }

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
                <div className="aspect-video bg-gray-700 rounded-lg flex items-center justify-center">
                  <div className="text-center text-gray-400">
                    <Video className="h-12 w-12 mx-auto mb-2" />
                    <p>Video preview will appear here</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <h4 className="font-semibold text-white">Available Features</h4>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Text-to-Video</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Image-to-Video</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Motion Control</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Style Transfer</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Auto-editing</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Transitions</div>
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

