export const dynamic = 'force-static'

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black py-20 px-6">
      <div className="container mx-auto prose prose-invert max-w-3xl">
        <h1>Privacy Policy</h1>
        <p>Last updated: August 12, 2025</p>
        <p>
          AEON Protocol ("AEON", "we", "us", or "our") is committed to protecting your privacy.
          This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you
          use our platform and services.
        </p>
        <h2>Information We Collect</h2>
        <ul>
          <li>Account information (name, email, organization)</li>
          <li>Authentication identifiers provided by our identity provider</li>
          <li>Usage data and device information for security and analytics</li>
          <li>Content and assets you create or upload to the platform</li>
        </ul>
        <h2>How We Use Information</h2>
        <ul>
          <li>Provide and maintain the AEON services</li>
          <li>Process payments, subscriptions, and invoices</li>
          <li>Improve features, performance, and security</li>
          <li>Comply with legal obligations</li>
        </ul>
        <h2>Data Sharing</h2>
        <p>
          We do not sell personal data. We may share information with trusted processors strictly
          to deliver the service (e.g., cloud hosting, storage, and payment processing partners) under
          data processing agreements.
        </p>
        <h2>International Transfers</h2>
        <p>
          Data may be processed in the United States and other jurisdictions with appropriate safeguards
          in place.
        </p>
        <h2>Security</h2>
        <p>
          We implement technical and organizational measures to protect your data, including encryption
          in transit, access controls, logging, and regular security reviews.
        </p>
        <h2>Your Rights</h2>
        <p>
          Depending on your location, you may have rights to access, correct, or delete your personal data.
          Contact us at privacy@aeonprotocol.com to exercise these rights.
        </p>
        <h2>Contact</h2>
        <p>privacy@aeonprotocol.com</p>
      </div>
    </div>
  )
}

