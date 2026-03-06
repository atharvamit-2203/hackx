/** @type {import('next').NextConfig} */
const nextConfig = {
  // No output: 'export' for Vercel - it handles SSR properly
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Ensure client components work properly
  reactStrictMode: true,
  webpack: (config, { isServer }) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': './src'
    };
    
    // Externalize Firebase on server-side
    if (isServer) {
      config.externals = config.externals || [];
      config.externals.push({
        'firebase/app': 'commonjs firebase/app',
        'firebase/auth': 'commonjs firebase/auth',
        'firebase/database': 'commonjs firebase/database',
      });
    }
    
    return config;
  }
};

export default nextConfig;
