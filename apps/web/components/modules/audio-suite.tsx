"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Loader2,
  Headphones,
  Mic,
  Music,
  Volume2,
  Settings,
  Sparkles,
  Languages,
  UserCheck
} from "lucide-react"

interface AudioSuiteProps {
  onGenerate: (data: any) => void
  isGenerating: boolean
}

export function AudioSuite({ onGenerate, isGenerating }: AudioSuiteProps) {
  const [text, setText] = useState("")
  const [voiceId, setVoiceId] = useState("21m00Tcm4TlvDq8ikWAM")
  const [stability, setStability] = useState([0.5])
  const [similarityBoost, setSimilarityBoost] = useState([0.5])
  const [style, setStyle] = useState([0])

  const handleGenerate = () => {
    onGenerate({
      text: text.trim(),
      voice_id: voiceId,
      stability: stability[0],
      similarity_boost: similarityBoost[0],
      style: style[0]
    })
  }

  const voices = [
    { id: "21m00Tcm4TlvDq8ikWAM", name: "Rachel", description: "Young, friendly female voice" },
    { id: "AZnzlk1XvdvUeBnXmlld", name: "Domi", description: "Strong, confident female voice" },
    { id: "EXAVITQu4vr4xnSDxMaL", name: "Bella", description: "Soft, warm female voice" },
    { id: "ErXwobaYiN019PkySvjV", name: "Antoni", description: "Deep, mature male voice" },
    { id: "VR6AewLTigWG4xSOukaG", name: "Arnold", description: "Crisp, authoritative male voice" },
    { id: "pNInz6obpgDQGcFmaJgB", name: "Adam", description: "Natural, conversational male voice" }
  ]

  const languages = [
    { code: "en", name: "English" },
    { code: "es", name: "Spanish" },
    { code: "fr", name: "French" },
    { code: "de", name: "German" },
    { code: "it", name: "Italian" },
    { code: "pt", name: "Portuguese" },
    { code: "pl", name: "Polish" },
    { code: "tr", name: "Turkish" },
    { code: "ru", name: "Russian" },
    { code: "nl", name: "Dutch" },
    { code: "cs", name: "Czech" },
    { code: "ar", name: "Arabic" },
    { code: "zh", name: "Chinese" },
    { code: "ja", name: "Japanese" },
    { code: "hi", name: "Hindi" },
    { code: "ko", name: "Korean" }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500">
          <Headphones className="h-8 w-8 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Audio Suite</h2>
          <p className="text-gray-400">Voice synthesis and audio processing</p>
        </div>
      </div>

      <Tabs defaultValue="tts" className="w-full">
        <TabsList className="grid w-full grid-cols-5 bg-gray-800">
          <TabsTrigger value="tts" className="data-[state=active]:bg-gray-700">
            <Mic className="h-4 w-4 mr-2" />
            Text-to-Speech
          </TabsTrigger>
          <TabsTrigger value="clone" className="data-[state=active]:bg-gray-700">
            <UserCheck className="h-4 w-4 mr-2" />
            Voice Clone
          </TabsTrigger>
          <TabsTrigger value="translate" className="data-[state=active]:bg-gray-700">
            <Languages className="h-4 w-4 mr-2" />
            Translate
          </TabsTrigger>
          <TabsTrigger value="music" className="data-[state=active]:bg-gray-700">
            <Music className="h-4 w-4 mr-2" />
            Music Gen
          </TabsTrigger>
          <TabsTrigger value="enhance" className="data-[state=active]:bg-gray-700">
            <Sparkles className="h-4 w-4 mr-2" />
            Enhance
          </TabsTrigger>
        </TabsList>

        <TabsContent value="tts" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Text-to-Speech Controls */}
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Mic className="h-5 w-5" />
                  Text-to-Speech Generation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Text Input */}
                <div className="space-y-2">
                  <Label className="text-white">Text to Convert</Label>
                  <textarea
                    placeholder="Enter the text you want to convert to speech. You can include SSML tags for advanced control over pronunciation, pauses, and emphasis..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    className="w-full min-h-[120px] p-3 bg-gray-700 border-gray-600 text-white rounded-md resize-none"
                  />
                  <p className="text-xs text-gray-400">
                    Character count: {text.length} / 5000
                  </p>
                </div>

                {/* Voice Selection */}
                <div className="space-y-2">
                  <Label className="text-white">Voice</Label>
                  <Select value={voiceId} onValueChange={setVoiceId}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      {voices.map((voice) => (
                        <SelectItem key={voice.id} value={voice.id} className="text-white">
                          <div>
                            <div className="font-medium">{voice.name}</div>
                            <div className="text-sm text-gray-400">{voice.description}</div>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Voice Settings */}
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-white">Stability: {(stability[0] || 0.5).toFixed(2)}</Label>
                    <Slider
                      value={stability}
                      onValueChange={setStability}
                      max={1}
                      min={0}
                      step={0.01}
                      className="w-full"
                    />
                    <p className="text-xs text-gray-400">
                      Higher values make the voice more stable but less expressive
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-white">Similarity Boost: {(similarityBoost[0] || 0.5).toFixed(2)}</Label>
                    <Slider
                      value={similarityBoost}
                      onValueChange={setSimilarityBoost}
                      max={1}
                      min={0}
                      step={0.01}
                      className="w-full"
                    />
                    <p className="text-xs text-gray-400">
                      Higher values make the voice more similar to the original
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-white">Style: {(style[0] || 0).toFixed(2)}</Label>
                    <Slider
                      value={style}
                      onValueChange={setStyle}
                      max={1}
                      min={0}
                      step={0.01}
                      className="w-full"
                    />
                    <p className="text-xs text-gray-400">
                      Higher values add more style and emotion to the voice
                    </p>
                  </div>
                </div>

                {/* Generate Button */}
                <Button 
                  onClick={handleGenerate} 
                  disabled={isGenerating || !text.trim()}
                  className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Generating Audio...
                    </>
                  ) : (
                    <>
                      <Volume2 className="h-4 w-4 mr-2" />
                      Generate Speech
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
                  Audio Preview & Features
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="aspect-video bg-gray-700 rounded-lg flex items-center justify-center">
                  <div className="text-center text-gray-400">
                    <Volume2 className="h-12 w-12 mx-auto mb-2" />
                    <p>Audio preview will appear here</p>
                    <div className="mt-4 w-full bg-gray-600 h-2 rounded-full">
                      <div className="bg-green-500 h-2 rounded-full w-0"></div>
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <h4 className="font-semibold text-white">Available Features</h4>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">ElevenLabs</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Voice Cloning</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">SSML Support</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Multi-language</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Emotion Control</div>
                    <div className="p-2 bg-gray-700 rounded text-sm text-gray-300">Speed Control</div>
                  </div>
                </div>

                <div className="space-y-2">
                  <h4 className="font-semibold text-white">Supported Languages</h4>
                  <div className="flex flex-wrap gap-1">
                    {languages.slice(0, 8).map((lang) => (
                      <span 
                        key={lang.code}
                        className="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded-full"
                      >
                        {lang.name}
                      </span>
                    ))}
                    <span className="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded-full">
                      +{languages.length - 8} more
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="clone" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🎭</div>
                <h3 className="text-2xl font-semibold text-white">Voice Cloning</h3>
                <p className="text-gray-400">
                  Clone any voice with just a few minutes of audio samples. Perfect for creating custom voices.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="translate" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🌍</div>
                <h3 className="text-2xl font-semibold text-white">Speech Translation</h3>
                <p className="text-gray-400">
                  Translate speech to any language while preserving the original voice characteristics.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="music" className="space-y-6">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <div className="space-y-4">
                <div className="text-6xl">🎵</div>
                <h3 className="text-2xl font-semibold text-white">Music Generation</h3>
                <p className="text-gray-400">
                  Generate custom music tracks, sound effects, and background audio for your projects.
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
                <h3 className="text-2xl font-semibold text-white">Audio Enhancement</h3>
                <p className="text-gray-400">
                  Enhance audio quality, remove noise, and apply professional audio processing effects.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
