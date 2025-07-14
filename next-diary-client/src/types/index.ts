// frontend/src/types/index.ts
export interface Comment {
  id: number
  author: string
  content: string
  created_at: string
}

export interface Diary {
  id: number
  author: string
  content: string
  created_at: string
  comments: Comment[]
}
