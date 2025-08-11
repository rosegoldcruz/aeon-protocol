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
  Palette,
  Wand2,
  Settings,
  Sparkles,
  Scissors,
  Maximize,
  Paintbrush
} from "lucide-react"

interface ImageStudioProps {
  onGenerate: (data: any) => void
  isGenerating: boolean
}

export function ImageStudio({ onGenerate, isGenerating }: ImageStudioProps) {
  const [prompt, setPrompt] = useState("")
  const [model, setModel] = useState("flux-schnell")
  const [width, setWidth] = useState([1024])
  const [height, setHeight] = useState([1024])
  const [numOutputs, setNumOutputs] = useState([1])
  const [guidance, setGuidance] = useState([7.5])
  const [steps, setSteps] = useState([20])
  const [seed, setSeed] = useState("")
  const [negativePrompt, setNegativePrompt] = useState("")

  const handleGenerate = () => {
    onGenerate({
      prompt: prompt.trim(),
      model,
      width: width[0],
      height: height[0],
      num_outputs: numOutputs[0],
      guidance_scale: guidance[0],
      num_inference_steps: steps[0],
      seed: seed ? parseInt(seed) : undefined,
      negative_prompt: negativePrompt.trim() || undefined
    })
  }

  const presetSizes = [
    { name: "Square", width: 1024, height: 1024 },
    { name: "Portrait", width: 768, height: 1024 },
    { name: "Landscape", width: 1024, height: 768 },
    { name: "Wide", width: 1344, height: 768 },
    { name: "Tall", width: 768, height: 1344 }
  ]

  const models = [
    { id: "flux-schnell", name: "FLUX Schnell", description: "Fast, high-quality generation" },
    { id: "flux-dev", name: "FLUX Dev", description: "Best quality, slower" },
    { id: "dall-e-3", name: "DALL-E 3", description: "OpenAI's latest model" },
    { id: "ideogram", name: "Ideogram", description: "Great for text in images" }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500">
          <Palette className="h-8 w-8 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Image Studio</h2>
          <p className="text-gray-400">AI-powered image generation and editing</p>
        </div>
      </div>

      <Tabs defaultValue="generate" className="w-full">
        <TabsList className="grid w-full grid-cols-4 bg-gray-800">
          <TabsTrigger value="generate" className="data-[state=active]:bg-gray-700">
            <Wand2 className="h-4 w-4 mr-2" />
            Generate
          </TabsTrigger>
          <TabsTrigger value="edit" className="data-[state=active]:bg-gray-700">
            <Paintbrush className="h-4 w-4 mr-2" />
            Edit
          </TabsTrigger>
          <TabsTrigger value="upscale" className="data-[state=active]:bg-gray-700">
            <Maximize className="h-4 w-4 mr-2" />
            Upscale
          </TabsTrigger>
          <TabsTrigger value="remove-bg" className="data-[state=active]:bg-gray-700">
            <Scissors className="h-4 w-4 mr-2" />
            Remove BG
          </TabsTrigger>
        </TabsList>

        <TabsContent value="generate" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Generation Controls */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Sparkles className="h-5 w-5" />
                  Generation Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Prompt */}
                <div className="space-y-2">
                  <Label className="text-white">Prompt</Label>
                  <Input
                    placeholder="A futuristic city at sunset with flying cars, highly detailed, 8k resolution..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>

                {/* Negative Prompt */}
                <div className="space-y-2">
                  <Label className="text-white">Negative Prompt (Optional)</Label>
                  <Input
                    placeholder="blurry, low quality, distorted..."
                    value={negativePrompt}
                    onChange={(e) => setNegativePrompt(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white"
                  />
                </div>

                {/* Model Selection */}
                <div className="space-y-2">
                  <Label className="text-white">Model</Label>
                  <Select value={model} onValueChange={setModel}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      {models.map((m) => (
                        <SelectItem key={m.id} value={m.id} className="text-white">
                          <div>
                            <div className="font-medium">{m.name}</div>
                            <div className="text-sm text-gray-400">{m.description}</div>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Size Presets */}
                <div className="space-y-2">
                  <Label className="text-white">Size Presets</Label>
                  <div className="grid grid-cols-3 gap-2">
                    {presetSizes.map((preset) => (
                      <Button
                        key={preset.name}
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setWidth([preset.width])
                          setHeight([preset.height])
                        }}
                        className="bg-gray-700 border-gray-600 text-white hover:bg-gray-600"
                      >
                        {preset.name}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Custom Dimensions */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label className="text-white">Width: {width[0]}px</Label>
                    <Slider
                      value={width}
                      onValueChange={setWidth}
                      max={1536}
                      min={512}
                      step={64}
                      className="w-full"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-white">Height: {height[0]}px</Label>
                    <Slider
                      value={height}
                      onValueChange={setHeight}
                      max={1536}
                      min={512}
                      step={64}
                      className="w-full"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Advanced Settings */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Advanced Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Number of Images */}
                <div className="space-y-2">
                  <Label className="text-white">Number of Images: {numOutputs[0]}</Label>
                  <Slider
                    value={numOutputs}
                    onValueChange={setNumOutputs}
                    max={4}
                    min={1}
                    step={1}
                    className="w-full"
                  />
                </div>

                {/* Guidance Scale */}
                <div className="space-y-2">
                  <Label className="text-white">Guidance Scale: {guidance[0]}</Label>
                  <Slider
                    value={guidance}
                    onValueChange={setGuidance}
                    max={20}
                    min={1}
                    step={0.5}
                    className="w-full"
                  />
                </div>

                {/* Inference Steps */}
                <div className="space-y-2">
                  <Label className="text-white">Inference Steps: {steps[0]}</Label>
                  <Slider
                    value={steps}
                    onValueChange={setSteps}
                    max={50}
                    min={10}
                    step={5}
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
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Wand2 className="h-4 w-4 mr-2" />
                      Generate Images
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="edit" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🎨</div>
                <h3 className="text-2xl font-semibold text-white">Image Editing</h3>
                <p className="text-gray-400">
                  Advanced image editing tools coming soon. Upload and edit images with AI-powered tools.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="upscale" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🔍</div>
                <h3 className="text-2xl font-semibold text-white">Image Upscaling</h3>
                <p className="text-gray-400">
                  AI-powered image upscaling and enhancement tools coming soon.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="remove-bg" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">✂️</div>
                <h3 className="text-2xl font-semibold text-white">Background Removal</h3>
                <p className="text-gray-400">
                  Automatic background removal and replacement tools coming soon.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
