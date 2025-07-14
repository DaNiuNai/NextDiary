<template>
  <el-card class="display-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>一封来自远方的日记</span>
        <el-button type="text" @click="$emit('new-exchange')">再换一封</el-button>
      </div>
    </template>

    <div class="diary-meta">
      <span>笔名：{{ diary.author }}</span>
      <span>时间：{{ new Date(diary.created_at).toLocaleString() }}</span>
    </div>

    <el-divider />

    <div class="diary-content" v-html="diary.content"></div>

    <el-divider>
      <span class="comment-divider-text">评论区</span>
    </el-divider>

    <div class="comment-section">
      <el-scrollbar max-height="200px">
        <div v-if="comments.length > 0">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <p>
              <strong>{{ comment.author }}</strong>
              <small>{{ new Date(comment.created_at).toLocaleString() }}</small>
            </p>
            <p>{{ comment.content }}</p>
          </div>
        </div>
        <el-empty v-else description="还没有评论，快来抢沙发吧！" />
      </el-scrollbar>
    </div>

    <div class="comment-form">
      <el-input v-model="newComment.author" placeholder="你的笔名" class="comment-input" />
      <el-input
        v-model="newComment.content"
        placeholder="留下你的足迹..."
        class="comment-input"
        type="textarea"
        :rows="2"
      />
      <el-button type="primary" @click="submitComment" :loading="isSubmittingComment">
        发表评论
      </el-button>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { PropType } from 'vue'
import type { Diary, Comment } from '@/types'
import { postComment } from '@/api'
import { ElMessage } from 'element-plus'

const props = defineProps({
  diary: {
    type: Object as PropType<Diary>,
    required: true,
  },
})

defineEmits(['new-exchange'])

const comments = ref<Comment[]>(props.diary.comments)
const isSubmittingComment = ref(false)
const newComment = reactive({
  author: '',
  content: '',
})

const submitComment = async () => {
  if (!newComment.author.trim() || !newComment.content.trim()) {
    ElMessage.warning('笔名和评论内容都不能为空')
    return
  }
  isSubmittingComment.value = true
  try {
    const createdComment = await postComment(props.diary.id, newComment.author, newComment.content)
    comments.value.push(createdComment)
    ElMessage.success('评论成功！')
    newComment.author = ''
    newComment.content = ''
  } catch (error) {
    ElMessage.error('评论失败')
    console.error(error)
  } finally {
    isSubmittingComment.value = false
  }
}
</script>

<style scoped>
.display-card {
  width: 800px;
  max-width: 90vw;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2em;
  font-weight: bold;
}
.diary-meta {
  display: flex;
  justify-content: space-between;
  color: #606266;
  font-size: 0.9em;
}
.diary-content {
  padding: 10px 0;
  line-height: 1.8;
  /* 确保编辑器上传的图片能正常显示 */
  :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }
}
.comment-divider-text {
  color: #909399;
}
.comment-item {
  border-bottom: 1px solid #e4e7ed;
  padding: 10px 0;
}
.comment-item:last-child {
  border-bottom: none;
}
.comment-item p {
  margin: 5px 0;
}
.comment-form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.comment-input {
  margin-bottom: 10px;
}
</style>
