import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowRight, Bot, Briefcase, Image, Sparkles } from "lucide-react"
import Link from "next/link"

// Force dynamic rendering to avoid static generation issues
export const dynamic = 'force-dynamic'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-black/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-8 w-8 text-blue-500" />
              <span className="text-2xl font-bold text-white">AEON</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/sign-in">
                <Button variant="ghost" className="text-white hover:text-blue-400">
                  Sign In
                </Button>
              </Link>
              <Link href="/sign-up">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto text-center">
          <h1 className="text-6xl font-bold text-white mb-6">
            The Complete
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600"> AI Stack</span>
            <br />for Enterprise
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            AEON is the unified AI business automation platform that replaces your entire tech stack. 
            Generate media, automate workflows, and scale your business with intelligent AI agents.
          </p>
          <div className="flex justify-center space-x-4">
            <Link href="/sign-up">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 bg-gray-900/50">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Everything You Need in One Platform</h2>
            <p className="text-xl text-gray-300">Replace your entire tech stack with AEON's unified AI ecosystem</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="bg-gray-800 border-gray-700 hover:border-blue-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <Image className="h-6 w-6 text-blue-400" />
                  </div>
                  <CardTitle className="text-white">Advanced Media Studio</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  Generate images, videos, and audio with cutting-edge AI models
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• FLUX, DALL-E, Ideogram integration</li>
                  <li>• Runway, Pika, Luma video generation</li>
                  <li>• ElevenLabs voice synthesis</li>
                  <li>• Batch processing & custom models</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700 hover:border-purple-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-500/20 rounded-lg">
                    <Bot className="h-6 w-6 text-purple-400" />
                  </div>
                  <CardTitle className="text-white">Intelligent AI Agents</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  Intelligent agents for content creation and business automation
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• Screenwriter & Video Editor agents</li>
                  <li>• Sales & Customer Service automation</li>
                  <li>• Marketing & Analytics insights</li>
                  <li>• SEO & Content optimization</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700 hover:border-green-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <Briefcase className="h-6 w-6 text-green-400" />
                  </div>
                  <CardTitle className="text-white">Enterprise Integration</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  Seamless integration with your existing business tools
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• CRM integration (HubSpot, Salesforce)</li>
                  <li>• E-commerce (Shopify, WooCommerce)</li>
                  <li>• ERP & workflow automation</li>
                  <li>• Custom API connections</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black border-t border-gray-800 py-12 px-6">
        <div className="container mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Sparkles className="h-6 w-6 text-blue-500" />
            <span className="text-xl font-bold text-white">AEON</span>
          </div>
          <p className="text-gray-400 mb-4">The Complete AI Operating System for Enterprise</p>
          <div className="flex justify-center space-x-6 text-sm text-gray-500">
            <span>© 2024 AEON Protocol</span>
            <span>•</span>
            <span>Enterprise AI Platform</span>
          </div>
        </div>
      </footer>
    </div>
  )
}
