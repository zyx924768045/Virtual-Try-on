import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
 plugins: [vue(),viteCompression({
  verbose: true,//是否在控制台输出压缩结果
  disable: false,//是否禁用,相当于开关在这里
  threshold: 10240,//体积大于 threshold 才会被压缩,单位 b，1b=8B, 1B=1024KB  这里相当于 9kb多，就会压缩
  algorithm: 'gzip',//压缩算法,可选 [ 'gzip' , 'brotliCompress' ,'deflate' , 'deflateRaw']
  ext: '.gz',//文件后缀
  }),
],
 base:'./',
 build: {
    outDir: 'dist', //输出目录名
    minify: 'esbuild',
    // chunkSizeWarningLimit: 1500,大文件报警阈值设置
    rollupOptions: {
      output: { //静态资源分类打包
        chunkFileNames: 'static/js/[name]-[hash].js',
        entryFileNames: 'static/js/[name]-[hash].js',
        assetFileNames: 'static/[ext]/[name]-[hash].[ext]',
        manualChunks(id) { //静态资源分拆打包
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString();
          }
        }
      }
    }
  },
  server: {
    host: '127.0.0.1'
  }
})