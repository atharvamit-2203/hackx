/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'export', // Disabled for now to allow client-side rendering
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': './src'
    };
    return config;
  }
};

export default nextConfig;
