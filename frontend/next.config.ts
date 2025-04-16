import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  basePath: '',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*` : 'http://localhost:8000/api/:path*',
      },
    ];
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NETLIFY_URL || process.env.URL || 'http://localhost:3000',
  },
  images: {
    domains: ['i.ytimg.com', 'yt3.ggpht.com'],
  },
  output: 'standalone',
};

export default nextConfig;
