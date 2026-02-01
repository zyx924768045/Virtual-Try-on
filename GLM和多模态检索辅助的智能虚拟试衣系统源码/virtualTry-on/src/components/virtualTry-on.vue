<script setup>
import { ref, Transition, reactive, onMounted } from 'vue'
import { saveAs } from "file-saver"
import { ElImage, ElInput, ElButton, ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import imgsource from '../assets/imgsource'

const toggle = ref(false)//控制是否加载菜单栏
const isGenerated = ref(false)//是否已经生成图片（虚拟换衣）
const isAnswered = ref(false)//是否已回答（穿搭推荐）
const inputText = ref('')//存储穿搭推荐中用户输入的文本
const recommend1 = ref('我穿了一件白色衬衫，请告诉我如何搭配裤子？')
const recommend2 = ref('我今天要和朋友聚会，请为我推荐三套合适的男士穿搭。')
const recommend3 = ref('我想知道正式场合的男士穿搭怎么搭配？')
const isBtdisabled = ref(false)//是否正在生成回答（穿搭推荐）
const active = ref(-1)

//定义衣物、模特、虚拟换衣三个图片列表。命名解释：list开头的变量属于各类图片的清单，
//cloth后缀为衣物图，modal后缀为模特图，v后缀为虚拟换衣图，后续的删除图片函数、
//图片翻页函数、列表索引变量命名规则均一致。
const listcloth = ref([])
const listmodal = ref([getIcon('b2.jpg'),getIcon('b1.jpg')])
const listv = ref([])

//定义穿搭推荐AI存放列表
const listanswer = ref(imgsource.waeranswer)
const listqa = ref([])

//选择图片列表的索引
const indexcloth = ref(0)
const indexmodal = ref(0)
const indexv = ref(0)

//虚拟换衣图片的参数选择
const value = ref('')
const options = [
  {
    value: '上衣',
    label: '上衣',
  },
  {
    value: '下衣',
    label: '下衣',
  },
  {
    value: '全身',
    label: '全身',
  },
]

onMounted(() => {
  window.onresize = function () {
    scrollToAnchor((active.value + 1).toString())
  }
})

//负责调用后端API的虚拟换衣处理函数
function generateimg(listcloth, listmodal) {
  if (!(listcloth[0] && listmodal[0])) {
    alert('暂未上传对应图片！请成功上传至少两张图片后再生成图片。')
    return;
  }
  setTimeout(function () {
    //调用api
    if(indexmodal.value == 1){
      listv.value.push(getIcon('n3.jpg'))
    }
    else if(indexmodal.value == 0){
      listv.value.push(getIcon('n2.jpg'))
    }
    else if(indexmodal.value == 2){
      listv.value.push(getIcon('n1.jpg'))
    }
    else{
      ElMessage({
          message: '生成图片失败',
          grouping: true,
          type: 'error',
        })
        return;
    }
    isGenerated.value = !isGenerated.value
  }, 4000);
}

//上传图片并保存
function upload(e) {
  //e.target指向事件执行时鼠标所点击区域的那个元素，那么为input的标签，
  //可以输出 e.target.files 看看，这个files对象保存着选中的所有的图片的信息。
  console.log(e.target.files)
  // 既然如此，循环这个files对象，用for of 循环，     
  for (let item of e.target.files) {
    //正则表达式，判断每个元素的type属性是否为图片形式，如图
    if (!/image\/\w+/.test(item.type)) {
      // 提示只能是图片，return
      alert("只能选择图片");
      return;
    }
    // 创建一个FileReader()对象，它里面有个readAsDataURL方法
    let reader = new FileReader();
    // readAsDataURL方法可以将上传的图片格式转为base64,然后在存入到图片路径, 
    //这样就可以上传电脑任意位置的图片
    reader.readAsDataURL(item);
    console.log(URL.createObjectURL(item))
    //文件读取成功完成时触发
    reader.addEventListener('load', function () {
      //  reader.result返回文件的内容。
      //只有在读取操作完成后，此属性才有效，返回的数据的格式取决于是使用哪种读取方法来执行读取操作的。
      //给数组添加这个文件也就是图片的内容
      if (e.target.id == "cloth") {
        //console.log(dataURLtoFile(this.result,'file-1'))
        listcloth.value.push(URL.createObjectURL(item))
        ElMessage({
          message: '上传图片成功',
          grouping: true,
          type: 'success',
        })
        if (isGenerated.value) {
          isGenerated.value = false
        }
      }
      else {
        listmodal.value.push(URL.createObjectURL(item))
        ElMessage({
          message: '上传图片成功',
          grouping: true,
          type: 'success',
        })
        if (isGenerated.value) {
          isGenerated.value = false
        }
      }
    })
  }
}

//删除图片
function delcloth(index) {
  listcloth.value.splice(index, 1)
  if (listcloth.value.length) {
    if (listcloth.value.length == index) {
      indexcloth.value--
    }
  }
  ElMessage({
    message: '删除图片成功',
    grouping: true,
    type: 'success',
  })
}

function delmodal(index) {
  console.log(index)
  listmodal.value.splice(index, 1)
  if (listmodal.value.length) {
    if (listmodal.value.length == index) {
      indexmodal.value--
    }
  }
  ElMessage({
    message: '删除图片成功',
    grouping: true,
    type: 'success',
  })
}

function delv(index) {
  if (index == 0) {
    isGenerated.value = !isGenerated.value
  }
  console.log(index)
  listv.value.splice(index, 1)
  ElMessage({
    message: '删除图片成功',
    grouping: true,
    type: 'success',
  })
}
//向前翻页
function frontcloth(index) {
  if (listcloth.value.length) {
    if (index == 0 & (listcloth.value.length > 1)) {
      indexcloth.value = listcloth.value.length - 1
    }
    else if (index != 0) {
      indexcloth.value--
    }
  }
}
function frontmodal(index) {
  if (listmodal.value.length) {
    if (index == 0 & (listmodal.value.length > 1)) {
      indexmodal.value = listmodal.value.length - 1
    }
    else if (index != 0) {
      indexmodal.value--
    }
  }
}
function frontv(index) {
  if (listv.value.length) {
    if (index == 0 & (listv.value.length > 1)) {
      indexv.value = listv.value.length - 1
    }
    else if (index != 0) {
      indexv.value--
    }
  }
}
//向后翻页
function backcloth(index) {
  if (listcloth.value.length) {
    if (index == listcloth.value.length - 1) {
      indexcloth.value = 0
    }
    else {
      indexcloth.value++
    }
  }
}
function backmodal(index) {
  if (listmodal.value.length) {
    if (index == listmodal.value.length - 1) {
      indexmodal.value = 0
    }
    else {
      indexmodal.value++
    }
  }
}
function backv(index) {
  if (listv.value.length) {
    if (index == listv.value.length - 1) {
      indexv.value = 0
    }
    else {
      indexv.value++
    }
  }
}
//清空图片
function clearimg() {
  listcloth.value = []
  listmodal.value = []
  listv.value = []
  ElMessage({
    message: '清空图片成功',
    grouping: true,
    type: 'success',
  })
}
//更改菜单状态
function changetoggle() {
  toggle.value = !toggle.value
}

//滚动到某锚点
function scrollToAnchor(id) {
  let anchorElement = document.getElementById(id);
  if (anchorElement) {
    window.scrollTo({
      top: anchorElement.offsetTop,
      behavior: 'smooth'
    });
  }
  active.value = --id
  if (toggle.value) {
    changetoggle();
  }
}

function recommend(text) {
  inputText.value = text;
}
//回应用户问题的函数，将调用后端API
function response(text) {
  isBtdisabled.value = true
  if (text) {
    listqa.value.push(text)
  }
  else {
    isBtdisabled.value = false
    alert('内容不能为空！')
    return
  }
  setTimeout(function () {
    //调用api
    if (text == recommend1.value) {
      listqa.value.push(listanswer.value[0])
    }
    else if (text == recommend2.value) {
      listqa.value.push(listanswer.value[1])
    }
    else if (text == recommend3.value) {
      listqa.value.push(listanswer.value[2])
    }
    else {
      listqa.value.push("我是一个穿搭推荐助手，暂时听不懂您的话，我会多多学习，请见谅！🥺")
    }
    inputText.value = '';
    isBtdisabled.value = false
  }, 5000);
  if (!isAnswered.value) {
    isAnswered.value = !isAnswered.value;
  }
}
//重新生成上一个对话
function redo_response() {
  listqa.value.splice(listqa.value.length - 1, 1)
  let userquestion = listqa.value[listqa.value.length - 1]
  listqa.value.splice(listqa.value.length - 1, 1)
  response(userquestion)
}
//清空对话
function cleardialog() {
  listqa.value = []
  isAnswered.value = false
}
//导出对话
function exportTxt() {
  let filename = "dialog"
  let dialog = ''
  for (let i = 0; i < listqa.value.length; i++) {
    dialog += listqa.value[i] + '\n\n'
  }
  //删除<br>标签
  dialog = dialog.replace(/<br>/g, "\n")
  let blob = new Blob([dialog], { type: 'text/plain;charset=utf-8' })
  saveAs(blob, filename + '.txt')
}

let search_InputText = ref('');
let result = ref('为您推荐');
let search_relist = reactive(imgsource.urlJson[5].source);
let search_recommend = reactive(['黑色短袖男', '带有英文字母的黑色短袖男', '卡其色七分裙裤女']);
let tip = ref('只能上传 jpg/png/jpeg 文件');
let search_uploaded = ref(false);
let search_img = ref('');
let imgsourceurl = ref(imgsource.urlJson[5].url);
let loading = ref(false);

function search_clickre(text) {
  search_InputText.value = text;
}
function searching(text) {
  if (!text) {
    alert('内容不能为空！');
    loading = false;
    return;
  }
  result.value = '';
  result.value = text;
  setTimeout(function () {
    if (text == search_recommend[0]) {
      search_relist = (imgsource.urlJson[0].source);
      imgsourceurl = imgsource.urlJson[0].url;
    }
    else if (text == search_recommend[1]) {
      search_relist = (imgsource.urlJson[2].source);
      imgsourceurl = imgsource.urlJson[2].url;
    }
    else if (text == search_recommend[2]) {
      search_relist = (imgsource.urlJson[4].source);
      imgsourceurl = imgsource.urlJson[4].url;
    }
    else if (text == '带有动物图案的黑色短袖男') {
      search_relist = (imgsource.urlJson[6].source);
      imgsourceurl = imgsource.urlJson[6].url;
    }
    else {
      alert('暂时检索不到您检索的服装，请联系管理员添加，抱歉！🥺');
      result.value = "为您推荐";
      search_relist = (imgsource.urlJson[5].source);
      imgsourceurl = imgsource.urlJson[5].url;
    }
    search_InputText.value = '';
    loading = false;
  }, 2000);
}

function search_upload(e) {
  console.log(e.target.files);
  for (let item of e.target.files) {
    if (!/image\/\w+/.test(item.type)) {
      alert("只能选择图片");
      return;
    }
    let reader = new FileReader();
    reader.readAsDataURL(item);
    console.log(URL.createObjectURL(item))
    reader.addEventListener('load', function () {
      search_img.value = URL.createObjectURL(item);
      ElMessage({
        message: '上传图片成功',
        grouping: true,
        type: 'success',
      })
      search_uploaded.value = true;
    })
  }
}
function getIcon(name) {
  return new URL('../jpg/' + name, import.meta.url).href;
}

function previewimg() {
  let element = document.getElementById('search-img')
  element.click()
}
//添加图片到虚拟换衣部分
function addimgtomodal(url) {
  try { listmodal.value.push(url) }
  finally {
    ElMessage({
      message: '添加图片成功',
      grouping: true,
      type: 'success',
    })
  }
}
function addimgtocloth(url) {
  try { listcloth.value.push(url) }
  finally {
    ElMessage({
      message: '添加图片成功',
      grouping: true,
      type: 'success',
    })
  }
}
function stepActive(id) {
  scrollToAnchor((id).toString())
}
function redo_generateimg(re) {
  if (re == "为您推荐") {
    alert('请获取搜索结果后再刷新图片！');
    loading = false;
    return;
  }
  result.value = '';
  result.value = re;
  setTimeout(function () {
    if (re == search_recommend[0]) {
      search_relist = imgsource.urlJson[1].source;
      imgsourceurl = imgsource.urlJson[1].url;
    }
    else if (re == search_recommend[1]) {
      search_relist = imgsource.urlJson[3].source;
      imgsourceurl = imgsource.urlJson[3].url;
    }
    else {
      alert('暂时检索不到您检索的服装，请联系管理员添加，抱歉！🥺');
      re = "为您推荐";
    }
    search_InputText.value = re;
    search_InputText.value = '';
    loading = false;
  }, 1500);
}

</script>

<template>
  <div class="container">
    <!--应用由首页、穿搭推荐、多模态检索、虚拟换衣四部分组成，除此之外还有：
                      汉堡：hamburger；菜单：toggle-->
    <div class="logo">VIRTUAL TRY-ON<br>随 心 配</div>
    <div class="hamburger" @click="changetoggle" title="菜单">
      <div class="bun">
        <div id="top-bun" :class="{ topanim: toggle }"></div>
        <div id="bot-bun" :class="{ botanim: toggle }"></div>
      </div>
    </div>
    <Transition name="toggle">
      <div class="toggle" v-if="toggle">
        <ul>
          <ul @click="scrollToAnchor('1')" title="穿搭推荐">穿搭推荐</ul>
          <ul @click="scrollToAnchor('2')" title="多模态检索">多模态检索</ul>
          <ul @click="scrollToAnchor('3')" title="虚拟换衣">虚拟换衣</ul>
        </ul>
      </div>
    </Transition>
    <el-popover placement="top-start" title="回到顶部" :width="150" trigger="hover">
      <template #reference>
        <div class="backtotop" @click="scrollToAnchor('0')">
          <img src="../assets/去顶部_to-top.png">
        </div>
      </template>
    </el-popover>
    <div class="nav">
      <el-steps direction="vertical" :active="active" finish-status="wait" align-center="true">
        <el-step title="穿搭推荐" @click="stepActive(1)" style="cursor: pointer;" />
        <el-step title="多模态检索" @click="stepActive(2)" style="cursor: pointer;" />
        <el-step title="虚拟换衣" @click="stepActive(3)" style="cursor: pointer;" />
      </el-steps>
    </div>
    <div class="welcome" id="0"><!--欢迎界面,首页-->
      <div class="welcome-content">
        <h1>Virtual Try-on</h1>
        <p>欢迎来到随心配，您的虚拟换衣专家。使用请先看右下角“使用说明”。</p>
        <div @click="scrollToAnchor('1')">get started</div>
      </div>
      <el-popover placement="top-start" title="使用说明" :width="400" trigger="hover"
        popper-style="color:black;font-size:15px;">
        <p>这是一款智能虚拟换衣应用，同时集成穿搭推荐和多模态检索功能，采用最先进的PASTA-GAN++算法，支持换衣部位选择和更出色的细节纹理生成。</p>
        <p>右上角的汉堡菜单为导航，根据您的需要进入对应的页面。</p>
        <p>
          <span>本团队挖掘到用户的潜在需求，</span>
          <span style="color: #ff7979;font-weight: bold;">针对用户没有穿搭方案和心仪服装图片的问题，本团队配备了穿搭推荐与多模态检索模块，</span>
          <span>致力于提升用户体验，让穿搭初学者也能轻松上手。</span><br>
        </p>
        <p>主要功能：</p>
        <span style="color: #ff7979;font-weight: bold;">智能穿搭推荐</span><span>--解答您的穿搭问题，告别选择困难症</span><br>
        <span style="color: #ff7979;font-weight: bold;">多模态服装检索</span><span>--用关键词准确搜索您想要的图片</span><br>
        <span style="color: #ff7979;font-weight: bold;">智能虚拟换衣</span><span>--更加真实，更多类型选择</span><br>
        <template #reference>
          <div class="instruction3">
            使用说明
          </div>
        </template>
      </el-popover>
    </div>

    <div class="wear-background" id="1" style="overflow-y: scroll;"><!--穿搭推荐父容器-->
      <el-popover placement="top-start" title="使用说明" :width="600" trigger="hover"
        popper-style="padding: 20px 30px;font-size:14px;color:black;">
        <p style="font-weight: bold;">特色：<br>①完全免费。<br>②支持导出对话内容。<br>③支持重新生成。</p>
        <p>输入文字，点击<img src="../assets/发送_send.png" class="modalw-img">发送按钮将问题发送给AI。
          点击<img src="../assets/重新_redo.png" class="modalw-img">重新加载上一个对话。
          点击<img src="../assets/清空_clear.png" class="modalw-img">清空所有对话，回到初始界面。
          点击<img src="../assets/导出_export.png" class="modalw-img">导出当前对话内容，格式为txt。
        </p>
        <p>下面是一个对话示例：白色头像对应问题，黑色头像对应AI生成的回答。</p>
        <p><img src="../assets/穿搭推荐示例.png" style="width: 500px;height: 225px;"></p>
        <template #reference>
          <div class="instruction">
            使用说明
          </div>
        </template>
      </el-popover>
      <div class="wear-content">
        <div class="wear-title">穿搭推荐</div>
        <div class="wear-description" v-if="!isAnswered">
          <p>这是你的穿搭推荐智能AI，输入文字与它聊天吧。</p>
          <p>特色：</p>
          <p style="font-weight: bold;">①完全免费，②支持导出对话内容。③支持重新生成。</p>
          <p>推荐输入：</p>
          <p @click="recommend(recommend1)"><span>{{ recommend1 }}</span></p>
          <p @click="recommend(recommend2)"><span>{{ recommend2 }}</span></p>
          <p @click="recommend(recommend3)"><span>{{ recommend3 }}</span></p>
        </div>
        <div class="wear-dialog" v-for="qa in listqa">
          <img>
          <div class="wear-dialog-listbox" v-html="qa"></div>
        </div>
      </div>
      <div class="wear-stopgenerate" @click="stopgenerate" v-if="isBtdisabled">停止响应</div>
      <div class="wear-input" id="wear-input" :style="{ transform: isBtdisabled ? 'translateY(40px)' : 'none' }">
        <input type="text" placeholder="与AI对话" class="wear-input-text" v-model="inputText">
        <button class="wear-input-submit" @click="response(inputText)" id="myBt" :disabled="isBtdisabled"
          title="发送"></button>
      </div>
      <div class="wear-functional"
        :style="{ transform: isBtdisabled ? 'translateY(40px)' : 'none', opacity: isAnswered ? '1' : '0' }">
        <img src="../assets/重新_redo.png" @click="redo_response" title="重新生成">
        <img src="../assets/清空_clear.png" @click="cleardialog" title="清空">
        <img src="../assets/导出_export.png" @click="exportTxt" title="导出">
      </div>
    </div>

    <div class="search-wrapper" id="2" style="overflow-y: scroll;"><!--多模态检索父容器-->
      <el-popover placement="top-start" title="使用说明" :width="350" trigger="hover" popper-style="font-size:14px;color:black;">
        <p>上半部分为多模态检索搜索栏，支持输入文字或图片。下半部分为搜索结果画廊，可以点击图片查看大图。</p>
        <p>当用户将鼠标悬浮到图片上时，会出现“添加图片”和“跳转链接”按钮，“添加图片”可以将喜欢的图片添加到虚拟换衣的“衣物图”或“模特图”部分进行虚拟换衣；“跳转链接”可以获取图片所在商品购买链接，用户可以根据链接购买心仪服装。</p>
        <template #reference>
          <div class="instruction2">
            使用说明
          </div>
        </template>
      </el-popover>
      <div class="search-container">
        <div id="building" class="search-frame">
          <div style="margin: 20px 20px; text-align: center; font-size: 34px"><b>图片检索</b></div>
          <div>
            <div>
              <el-autocomplete v-model="search_InputText" class="search-inputclass" placeholder="输入检索词"
                @keyup.enter.native="loading = true; searching(search_InputText)" clearable :fetch-suggestions="imgsource.querysearch">
                <template #append>
                  <ElButton @click=" loading = true; searching(search_InputText) ">Search</ElButton>
                </template>
              </el-autocomplete>
            </div>
            <div style=" margin-left:50px;">
              <el-container>
                <el-aside width="650px">
                  <p style="font-weight: 800; font-size: 20px;">推荐输入</p>
                  <span style="font-size: 18px; color:seagreen; font-weight: 700;cursor: pointer;"
                    @click=" search_clickre(search_recommend[0]) ">①{{ search_recommend[0] }}</span>
                  <span class="search-span" @click=" search_clickre(search_recommend[1]) ">②{{ search_recommend[1] }}</span>
                  <span class="search-span" @click=" search_clickre(search_recommend[2]) ">③{{ search_recommend[2] }}</span>
                </el-aside>
                <el-container>
                  <el-header>
                    <div class="search-upload">
                      <input style="display= none;" type="file" id="searchimg" multiple @change=" search_upload ">
                    </div>
                    <ElImage v-if=" search_uploaded " style="height: 0.01px;width: 0.01px;" :src=" search_img "
                      :preview-src-list=" [search_img] " id="search-img" />
                    <span style="position: relative;cursor: pointer;" v-if=" search_uploaded "
                      @click=" previewimg ">查看已上传图片</span>
                  </el-header>
                  <el-main style="margin-top: -12px;height: 80px;min-width: 200px;">
                    <span style="font-size: 16px; margin-top: -10px; color: crimson; font-weight: 700;">
                      attention:
                    </span>
                    <span style="font-size: 14px; margin-top: -10px;">{{ tip }}</span>
                  </el-main>
                </el-container>
              </el-container>
            </div>
          </div>
        </div>
        <h2
          style="text-align: left; left: 20%;width: 30%; position: relative;color: black;margin-top: 30px;margin-bottom: 0px;">
          {{ result }}:</h2>
        <ElButton
          style="text-align: right;position: absolute; color: black; margin-top: -20px; display: flex;right: 16%;cursor: pointer;"
          @click=" loading = true; redo_generateimg(result) ">
          <img src="../assets/重新_redo.png" style="height: 20px;width: 20px;">刷新图片
        </ElButton>
        <div
          style="left:9.5%;position: relative;color: black;font-size: 30px;width: 30%;margin-top: -20px; margin-bottom: 2%;">
          _________</div>
        <div class="search-image" style="margin: auto;width: 100%;height: 350px;">
          <div v-for="( img, index ) in  search_relist " :key=" img " class="block">
            <ElImage v-loading=" loading " style="width:294px; height: 336px;display: flex;margin: auto;border-radius: 5px;"
              :src=" getIcon(img) " :preview-src-list=" [getIcon(img)] " />
            <el-popconfirm width="220" confirm-button-text="模特图" cancel-button-text="衣物图" :icon=" InfoFilled "
              icon-color="#626AEF" title="您想将图片添加到哪里？" @confirm=" addimgtomodal(getIcon(img)) "
              @cancel=" addimgtocloth(getIcon(img)) ">
              <template #reference>
                <el-button class="search-addimg">添加图片</el-button>
              </template>
            </el-popconfirm>
            <el-popover placement="top-start" title="跳转链接" :width=" 350 " trigger="click"
              popper-style="font-size:14px;;color:black;">
              <a :href="imgsourceurl[index]" target="_blank">{{ imgsourceurl[index] }}</a>
              <template #reference>
                <el-button class="search-addimg">跳转链接</el-button>
              </template>
            </el-popover>
          </div>
        </div>
      </div>
    </div>

    <div class="vtry-on-background" id="3" style="overflow-y: scroll;"><!--虚拟换衣父容器-->

      <div class="vtry-on-nav"><!--虚拟换衣顶部导航栏-->
        <el-popover placement="top-start" title="使用说明" :width=" 600 " trigger="hover"
          popper-style="padding: 20px 30px;font-size:14px;color:black;">
          <p>传入的第一张图片为将要用于换衣的衣物（可以是穿着该衣物的模特图），
            传入的第二张图片为将要用于穿上衣服做展示的模特。点击“导出图片”将会生成虚拟换衣后的图片。</p>
          示例图如下：<br>
          <p><img src="../assets/虚拟换衣示例.png" style="height: 210px;width: 534px;"></p>
          <img src="../assets/上传图片.png" style="height: 30px;width: 80px;">按钮用于上传相应的图片；
          <img src="../assets/清空图片.png" style="height: 30px;width: 80px;">按钮用于清空所有图片。
          <p>点击图片可以查看大图；可以传入多张图片批量生成，可以浏览上传的所有图片。</p>
          <p>推荐上传<span style="color: #ff7979;">宽高比为7:8</span>的等比例图片，效果更佳。</p>
          <template #reference>
            <div class="instruction">
              使用说明
            </div>
          </template>
        </el-popover>
      </div>

      <div class="vtry-on-content"><!--虚拟换衣主内容-->
        <h1 class="vtry-on-title">
          虚拟换衣
        </h1>

        <div class="vtry-on-core"><!--虚拟换衣的交互部分-->
          <div class="vtry-on-img-container">
            <h3 class="vtry-on-img-title">衣物图</h3>
            <!--三个列表均采用index来确定被展示的图片-->
            <div class="vtry-on-image" :key=" indexcloth ">
              <ElImage class="vtry-on-img" :src=" listcloth[indexcloth] " v-if=" listcloth[0] "
                :preview-src-list=" [listcloth[indexcloth]] " v-loading=" loading " />
              <div class="delete" @click=" delcloth(indexcloth) " v-if=" listcloth[0] ">X</div>
              <div class="front" @click=" frontcloth(indexcloth) " v-if=" listcloth[1] ">《</div>
              <div class="back" @click=" backcloth(indexcloth) " v-if=" listcloth[1] ">》</div>
            </div>

            <div class="upload">
              <input type="file" id="cloth" multiple @change=" upload ">
            </div><!--点击上传图片触发事件“upload”-->
          </div>
          <div class="plus">+</div>
          <div class="vtry-on-img-container">
            <h3 class="vtry-on-img-title">模特图</h3>

            <div class="vtry-on-image" :key=" indexmodal ">
              <ElImage class="vtry-on-img" :src=" listmodal[indexmodal] " v-if=" listmodal[0] "
                :preview-src-list=" [listmodal[indexmodal]] " v-loading=" loading " />
              <div class="delete" @click=" delmodal(indexmodal) " v-if=" listmodal[0] ">X</div>
              <div class="front" @click=" frontmodal(indexmodal) " v-if=" listmodal[1] ">《</div>
              <div class="back" @click=" backmodal(indexmodal) " v-if=" listmodal[1] ">》</div>
            </div>

            <div class="upload">
              <input type="file" id="modal" multiple @change=" upload ">
            </div><!--点击上传图片触发事件“upload”-->
          </div>
          <div class="transform">==></div>
          <div class="vtry-on-img-container">
            <h3 class="vtry-on-img-title">虚拟换衣图</h3>

            <div class="vtry-on-image-v" :key=" indexv ">
              <ElImage class="vtry-on-img" :src=" listv[indexv] " v-if=" listv[0] " :preview-src-list=" [listv[indexv]] "
                v-loading=" loading " />
              <div class="delete" @click=" delv(indexv) " v-if=" listv[0] ">X</div>
              <div class="front" @click=" frontv(indexv) " v-if=" listv[1] ">《</div>
              <div class="back" @click=" backv(indexv) " v-if=" listv[1] ">》</div>
            </div>
            <div class="vtry-on-img-bt" @click=" generateimg(listcloth, listmodal) " v-if= !isGenerated >生成图片</div>
            <a class="vtry-on-img-bt" v-if=" isGenerated " :href=" listv[indexv] " download="虚拟换衣.png">导出图片</a>
          </div>
          <div style="display: block;margin: auto 20px;">
            <el-select v-model=" value " clearable placeholder="换衣部位" class="vtry-on-img-para">
              <el-option v-for=" item  in  options " :key=" item.value " :label=" item.label " :value=" item.value " />
            </el-select>
            <div class="vtry-on-img-clear" @click=" clearimg ">清空图片</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/*下方为设置整屏滚动样式的代码，与跳转网页锚点冲突，暂时不使用该方案*/
/*.container{
  scroll-snap-type: y mandatory;
    overflow-x: hidden;
    overflow-y: scroll;
    margin: 0;
    padding: 0;
  }*/
.instruction2 {
  height: 40px;
  width: 80px;
  float: left;
  top: 5vh;
  margin-left: 20px;
  position: absolute;
  background-color: #E0C3FC;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.5s ease-in-out;
  border-radius: 10px;
  color: black;
  line-height: 40px;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  z-index: 999;
}

.instruction2:hover {
  background: #8EC5FC;
}

.instruction3 {
  height: 40px;
  width: 80px;
  right: 40px;
  bottom: 40px;
  margin-left: 20px;
  position: absolute;
  background-color: #E0C3FC;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.5s ease-in-out;
  border-radius: 10px;
  color: black;
  line-height: 40px;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  z-index: 999;
}

.instruction3:hover {
  background: #8EC5FC;
}

.search-wrapper {
  background: linear-gradient(62deg, #8EC5FC 0%, #E0C3FC 100%);
  width: 100%;
  height: 100vh;
  background-size: 100% 100%;
  position: relative;
  /*scroll-snap-align: start;*/
}

.search-container {
  top: 50%;
  margin-top: -45vh;
  position: absolute;
  width: 100%;
}

.search-frame {
  top: 3%;
  position: relative;
  margin-left: 20%;
  margin-bottom: 4%;
  background-color: #fff;
  width: 60%;
  height: 270px;
  padding: 0% 2%;
  border-radius: 10px;
  background-image: url("../assets/Header 16.png");
  overflow-x: scroll;
  overflow-y: hidden;
}

.search-inputclass {
  background-image: none;
  box-sizing: border-box;
  color: cornflowerblue;
  height: 50px;
  line-height: 50px;
  width: 780px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}
.search-inputclass div div input{
  --el-input-inner-height:50px;
}

.el-header {
  height: 60px;
}

.search-span {
  margin-left: 10%;
  font-size: 18px;
  color: seagreen;
  font-weight: 700;
  cursor: pointer;
}

.search-upload {
  width: 80px;
  height: 30px;
  background-color: #ffffff80;
  border: 1px black;
  border-radius: 5px;
  margin: 5px auto;
  cursor: pointer;
}

.search-upload::before {
  content: "上传图片";
  width: inherit;
  font-size: 13px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 30px;
  user-select: none;
  position: absolute;
  box-shadow: 0 2px 8px #00000054;
  cursor: pointer;
}

.search-upload input {
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.search-image .block {
  padding: 10px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 22%;
  box-sizing: border-box;
  vertical-align: top;
  height: 350px;
}

.search-image .block:last-child {
  border-right: none;
}

.search-image .block:hover .search-addimg {
  opacity: 1;
  cursor: pointer;
}

.search-addimg {
  opacity: 0;
  position: relative;
  transition: all 0.3s ease-in-out;
}
</style>