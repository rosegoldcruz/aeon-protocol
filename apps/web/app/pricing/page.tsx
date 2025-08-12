import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export const dynamic = 'force-static'

const plans = [
  {
    name: "Starter",
    price: "$29/mo",
    description: "For individuals getting started",
    features: [
      "Basic media generation",
      "100 image credits",
      "5 video credits",
      "Standard support"
    ],
    cta: { label: "Get Started", href: "/sign-up" }
  },
  {
    name: "Professional",
    price: "$99/mo",
    description: "For teams and growing businesses",
    features: [
      "Advanced media suite",
      "2,000 image credits",
      "100 video credits",
      "Priority support",
      "Agent automations"
    ],
    cta: { label: "Upgrade", href: "/sign-up" }
  },
  {
    name: "Enterprise",
    price: "Custom",
    description: "For organizations at scale",
    features: [
      "Unlimited team members",
      "Custom model hosting",
      "On-prem / Hybrid options",
      "Dedicated support & SLA"
    ],
    cta: { label: "Contact Sales", href: "mailto:sales@aeonprotocol.com" }
  }
]

export default function PricingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black py-20 px-6">
      <div className="container mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">Pricing</h1>
          <p className="text-gray-300">Choose the plan that fits your stage. Upgrade anytime.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <Card key={plan.name} className="bg-gray-900/60 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white flex items-baseline justify-between">
                  <span>{plan.name}</span>
                  <span className="text-2xl">{plan.price}</span>
                </CardTitle>
                <CardDescription className="text-gray-300">{plan.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-gray-300 space-y-2 mb-6">
                  {plan.features.map((f) => (
                    <li key={f}>• {f}</li>
                  ))}
                </ul>
                <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white" asChild>
                  <Link href={plan.cta.href}>{plan.cta.label}</Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12 text-sm text-gray-400">
          <Link href="/terms" className="hover:text-white">Terms</Link>
          <span className="mx-2">•</span>
          <Link href="/privacy" className="hover:text-white">Privacy</Link>
        </div>
      </div>
    </div>
  )
}

