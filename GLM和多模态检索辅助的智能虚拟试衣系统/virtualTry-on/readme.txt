virtualTry-on文件夹为“随心配”智能虚拟换衣系统的项目文件夹。
该项目基于Vue 3 + Vite 4.3.0 开发。以下为文件说明：
1.node_modules文件夹为项目安装的依赖，由于它属于公共类库，此处没有上传，是一个空文件夹。如果要让该项目正常运行，需要先安装依赖。
2.public文件夹为公共资源文件夹，存放一些公共资源。
3.src文件夹为项目的部分静态js、css资源以及项目的核心vue文件，保障项目的核心功能正常运行。
4.“.gitignore”为git相关文件，用于项目版本控制和协作开发。
5.home.css、vtry-on.css、wear.css均属于项目不同模块的css样式表文件。
6.index.html为项目开发版本的网站入口。
7.package-lock.json和package.json为项目开发的配置文件，控制项目的基本信息、指令集和依赖。
8.vite.config.js为vite项目使用rollup工具打包的配置文件，决定了项目打包的处理参数，包括体积压缩、大文件拆分打包、分类打包。