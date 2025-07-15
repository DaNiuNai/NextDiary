// frontend/src/api/index.ts
import axios from 'axios'
import type { Diary } from '@/types'

export const baseUrl = 'http://127.0.0.1:8080'

const apiClient = axios.create({
  baseURL: baseUrl, // 你的 FastAPI 后端地址
  headers: {
    'Content-Type': 'application/json',
  },
})

// 上传图片接口
export const uploadImage = async (file: File): Promise<{ url: string }> => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await apiClient.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// 交换日记接口
export const exchangeDiary = async (author: string, content: string): Promise<Diary> => {
  const response = await apiClient.post('/diary/exchange', { author, content })
  return response.data
}

// 发表评论接口
export const postComment = async (diaryId: number, author: string, content: string) => {
  const response = await apiClient.post(`/diary/add-comments/`, { author, content, diary_id: diaryId })
  return response.data
}
