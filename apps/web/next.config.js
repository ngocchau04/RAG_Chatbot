/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  experimental: {
    typedRoutes: true,
  },
  async rewrites() {
    const apiBase = process.env.API_INTERNAL_BASE_URL || "http://localhost:8000";
    return [
      {
        source: "/backend/:path*",
        destination: `${apiBase}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
