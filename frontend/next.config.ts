import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  basePath: '',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://youtube-research-backend.onrender.com/api/:path*',
      },
    ];
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://youtube-research-backend.onrender.com',
  },
  images: {
    domains: ['i.ytimg.com', 'yt3.ggpht.com'],
  },
};

export default nextConfig;
