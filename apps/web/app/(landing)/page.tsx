"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowRight, Bot, Briefcase, Image, Video, Music, Zap, Shield, Globe, Users, TrendingUp, Sparkles } from "lucide-react"
import Link from "next/link"

export default function LandingPage() {
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
            <Button size="lg" variant="outline" className="border-gray-600 text-white hover:bg-gray-800 px-8 py-4 text-lg">
              Watch Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 bg-gray-900/50">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-12">
            Everything You Need in One Platform
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Media Generation */}
            <Card className="bg-gray-800 border-gray-700 hover:border-blue-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Image className="h-8 w-8 text-blue-500" />
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

            {/* AI Agents */}
            <Card className="bg-gray-800 border-gray-700 hover:border-purple-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Bot className="h-8 w-8 text-purple-500" />
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
            <Card className="bg-gray-800 border-gray-700 hover:border-green-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Briefcase className="h-8 w-8 text-green-500" />
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

            {/* Collaboration */}
            <Card className="bg-gray-800 border-gray-700 hover:border-yellow-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Users className="h-8 w-8 text-yellow-500" />
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
            <Card className="bg-gray-800 border-gray-700 hover:border-red-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Shield className="h-8 w-8 text-red-500" />
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
            <Card className="bg-gray-800 border-gray-700 hover:border-cyan-500 transition-colors">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Zap className="h-8 w-8 text-cyan-500" />
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

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join thousands of companies using AEON to automate their workflows and scale with AI.
          </p>
          <Link href="/sign-up">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 text-lg">
              Start Your Free Trial
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-6">
        <div className="container mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-6 w-6 text-blue-500" />
              <span className="text-xl font-bold text-white">AEON</span>
            </div>
            <p className="text-gray-400">
              © 2025 AEON Protocol. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
