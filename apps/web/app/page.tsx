"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowRight, Bot, Briefcase, Image, Video, Zap, Shield, Globe, Users, TrendingUp, Sparkles, Play, CheckCircle, Star, Cpu } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-black/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-8 w-8 text-blue-500" />
              <span className="text-2xl font-bold text-white">AEON</span>
              <span className="text-sm bg-blue-600 px-2 py-1 rounded-full">AI Platform</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#features" className="text-gray-300 hover:text-white transition-colors">Features</Link>
              <Link href="#agents" className="text-gray-300 hover:text-white transition-colors">AI Agents</Link>
              <Link href="#integrations" className="text-gray-300 hover:text-white transition-colors">Integrations</Link>
              <Link href="#pricing" className="text-gray-300 hover:text-white transition-colors">Pricing</Link>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/sign-in">
                <Button variant="ghost" className="text-white hover:text-blue-400">
                  Sign In
                </Button>
              </Link>
              <Link href="/sign-up">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Start Free Trial
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20 blur-3xl"></div>
        <div className="container mx-auto text-center relative z-10">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
              The Complete
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-cyan-400"> AI Stack</span>
              <br />for Enterprise
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              AEON is the unified AI business automation platform that replaces your entire tech stack.
              Generate media, automate workflows, and scale your business with intelligent AI agents.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
              <Link href="/sign-up">
                <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button size="lg" variant="outline" className="border-gray-600 text-white hover:bg-gray-800 px-8 py-4 text-lg">
                <Play className="mr-2 h-5 w-5" />
                Watch Demo
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center items-center gap-8 text-gray-400 text-sm">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>SOC 2 Compliant</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-blue-500" />
                <span>Enterprise Security</span>
              </div>
              <div className="flex items-center gap-2">
                <Star className="h-4 w-4 text-yellow-500" />
                <span>99.9% Uptime</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 px-6 bg-gray-900/50">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Everything You Need in One Platform
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Replace multiple specialized tools with AEON's unified AI business automation platform
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Advanced Media Studio */}
            <Card className="bg-gray-800 border-gray-700 hover:border-blue-500 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/20">
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

            {/* AI Agent Ecosystem */}
            <Card className="bg-gray-800 border-gray-700 hover:border-purple-500 transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/20">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-500/20 rounded-lg">
                    <Bot className="h-6 w-6 text-purple-400" />
                  </div>
                  <CardTitle className="text-white">AI Agent Ecosystem</CardTitle>
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

            {/* Business Integration */}
            <Card className="bg-gray-800 border-gray-700 hover:border-green-500 transition-all duration-300 hover:shadow-xl hover:shadow-green-500/20">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <Briefcase className="h-6 w-6 text-green-400" />
                  </div>
                  <CardTitle className="text-white">Business Integration</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  Connect with your existing tools and workflows
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• CRM: HubSpot, Salesforce, Pipedrive</li>
                  <li>• E-commerce: Shopify, WooCommerce</li>
                  <li>• ERP & Operations automation</li>
                  <li>• Custom webhook integrations</li>
                </ul>
              </CardContent>
            </Card>

            {/* Real-time Collaboration */}
            <Card className="bg-gray-800 border-gray-700 hover:border-yellow-500 transition-all duration-300 hover:shadow-xl hover:shadow-yellow-500/20">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-yellow-500/20 rounded-lg">
                    <Users className="h-6 w-6 text-yellow-400" />
                  </div>
                  <CardTitle className="text-white">Real-time Collaboration</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  Work together seamlessly with your team
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• Figma-style collaborative editing</li>
                  <li>• Role-based permissions</li>
                  <li>• Approval pipelines</li>
                  <li>• Version control & rollback</li>
                </ul>
              </CardContent>
            </Card>

            {/* Enterprise Security */}
            <Card className="bg-gray-800 border-gray-700 hover:border-red-500 transition-all duration-300 hover:shadow-xl hover:shadow-red-500/20">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-red-500/20 rounded-lg">
                    <Shield className="h-6 w-6 text-red-400" />
                  </div>
                  <CardTitle className="text-white">Enterprise Security</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  SOC 2 compliant with enterprise-grade security
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• Multi-tenant data isolation</li>
                  <li>• GDPR/CCPA compliance</li>
                  <li>• Enterprise SSO integration</li>
                  <li>• Comprehensive audit logging</li>
                </ul>
              </CardContent>
            </Card>

            {/* Custom AI Training */}
            <Card className="bg-gray-800 border-gray-700 hover:border-cyan-500 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-500/20">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-cyan-500/20 rounded-lg">
                    <Zap className="h-6 w-6 text-cyan-400" />
                  </div>
                  <CardTitle className="text-white">Custom AI Training</CardTitle>
                </div>
                <CardDescription className="text-gray-300">
                  Train and deploy your own AI models
                </CardDescription>
              </CardHeader>
              <CardContent className="text-gray-400">
                <ul className="space-y-2">
                  <li>• Fine-tune LLMs & diffusion models</li>
                  <li>• Private model hosting</li>
                  <li>• Dataset ingestion tools</li>
                  <li>• Performance monitoring</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section id="agents" className="py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Intelligent AI Agent Ecosystem
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Deploy specialized AI agents that automate your entire business workflow
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: "Screenwriter", icon: Bot, color: "blue", desc: "Script generation & story analysis" },
              { name: "Video Editor", icon: Video, color: "green", desc: "Automated editing & pacing" },
              { name: "Sales Agent", icon: TrendingUp, color: "purple", desc: "Lead qualification & proposals" },
              { name: "Marketing", icon: Globe, color: "orange", desc: "Campaign creation & optimization" },
              { name: "Customer Service", icon: Users, color: "pink", desc: "Multi-channel support automation" },
              { name: "Analytics", icon: Cpu, color: "indigo", desc: "Cross-platform data insights" },
              { name: "SEO Content", icon: Sparkles, color: "yellow", desc: "Automated content optimization" },
              { name: "Content Optimizer", icon: Zap, color: "red", desc: "Performance prediction & A/B testing" }
            ].map((agent, index) => (
              <Card key={index} className="bg-gray-800 border-gray-700 hover:border-gray-600 transition-all duration-300 text-center p-6">
                <div className={`p-3 bg-${agent.color}-500/20 rounded-full w-fit mx-auto mb-4`}>
                  <agent.icon className={`h-8 w-8 text-${agent.color}-400`} />
                </div>
                <h3 className="text-white font-semibold text-lg mb-2">{agent.name}</h3>
                <p className="text-gray-400 text-sm">{agent.desc}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-blue-600/20 to-purple-600/20">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join thousands of companies using AEON to automate their workflows and scale with AI.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/sign-up">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 text-lg">
                Start Your Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline" className="border-gray-600 text-white hover:bg-gray-800 px-12 py-4 text-lg">
                View Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-6">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Sparkles className="h-6 w-6 text-blue-500" />
                <span className="text-xl font-bold text-white">AEON</span>
              </div>
              <p className="text-gray-400">
                The complete AI stack for enterprise business automation.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
                <li><Link href="/studio" className="hover:text-white transition-colors">Media Studio</Link></li>
                <li><Link href="/agents" className="hover:text-white transition-colors">AI Agents</Link></li>
                <li><Link href="/integrations" className="hover:text-white transition-colors">Integrations</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="/careers" className="hover:text-white transition-colors">Careers</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
                <li><Link href="/blog" className="hover:text-white transition-colors">Blog</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/docs" className="hover:text-white transition-colors">Documentation</Link></li>
                <li><Link href="/help" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="/status" className="hover:text-white transition-colors">Status</Link></li>
                <li><Link href="/security" className="hover:text-white transition-colors">Security</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400">
              © 2025 AEON Protocol. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">Privacy</Link>
              <Link href="/terms" className="text-gray-400 hover:text-white transition-colors">Terms</Link>
              <Link href="/cookies" className="text-gray-400 hover:text-white transition-colors">Cookies</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}