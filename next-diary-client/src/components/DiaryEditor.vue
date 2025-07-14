<template>
  <el-card class="editor-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>在字里行间，与世界温柔相拥。</span>
      </div>
    </template>

    <el-form :model="form" label-position="top">
      <el-form-item label="你的笔名">
        <el-input v-model="form.author" placeholder="一个独特的笔名" />
      </el-form-item>
      <el-form-item label="日记内容">
        <div style="border: 1px solid #ccc">
          <Toolbar
            style="border-bottom: 1px solid #ccc"
            :editor="editorRef"
            :defaultConfig="toolbarConfig"
            mode="default"
          />
          <Editor
            style="height: 300px; overflow-y: hidden"
            v-model="form.content"
            :defaultConfig="editorConfig"
            mode="default"
            @onCreated="handleCreated"
          />
        </div>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          @click="submitDiary"
          :loading="isLoading"
          class="submit-btn"
          size="large"
        >
          写给未来的陌生人
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, shallowRef, onBeforeUnmount } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import type { IEditorConfig, IToolbarConfig } from '@wangeditor/editor'
import { ElMessage } from 'element-plus'
import '@wangeditor/editor/dist/css/style.css'
import { exchangeDiary, uploadImage } from '@/api'
import type { Diary } from '@/types'

type InsertFnType = (url: string, alt: string, href: string) => void

const emit = defineEmits<{
  (e: 'submitted', diary: Diary): void
}>()

// --- Wangeditor 配置 ---
const editorRef = shallowRef()
const form = reactive({
  author: '',
  content: '<p>今天发生了什么有趣的事呢？</p>',
})
const isLoading = ref(false)

const toolbarConfig: Partial<IToolbarConfig> = {}
const editorConfig: Partial<IEditorConfig> = {
  placeholder: '请输入内容...',
  MENU_CONF: {
    uploadImage: {
      // 自定义上传
      async customUpload(file: File, insertFn: InsertFnType) {
        try {
          const res = await uploadImage(file)
          // WangEditor 需要完整的 URL
          const fullUrl = `http://127.0.0.1:8000${res.url}`
          insertFn(fullUrl, file.name, fullUrl)
          ElMessage.success('图片上传成功')
        } catch (error) {
          ElMessage.error('图片上传失败')
          console.error(error)
        }
      },
    },
  },
}

const handleCreated = (editor: any) => {
  editorRef.value = editor
}

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

// --- 业务逻辑 ---
const submitDiary = async () => {
  if (!form.author.trim()) {
    ElMessage.warning('请输入你的笔名')
    return
  }
  if (!form.content.trim() || form.content === '<p><br></p>') {
    ElMessage.warning('日记内容不能为空')
    return
  }

  isLoading.value = true
  try {
    const receivedDiary = await exchangeDiary(form.author, form.content)
    ElMessage.success('交换成功！')
    emit('submitted', receivedDiary)
  } catch (error: any) {
    if (error.response && error.response.data.detail) {
      ElMessage.error(`交换失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('交换失败，请稍后再试')
    }
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.editor-card {
  width: 800px;
  max-width: 90vw;
}
.card-header {
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
}
.submit-btn {
  width: 100%;
}
</style>
