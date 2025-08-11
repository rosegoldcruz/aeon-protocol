import { getComments, insertComment } from '@/lib/db'
import { revalidatePath } from 'next/cache'

export default async function CommentsPage() {
  // Server Action to create a comment
  async function create(formData: FormData) {
    'use server'
    
    const comment = formData.get('comment') as string
    
    // Validate comment
    if (!comment || comment.trim().length === 0) {
      return
    }

    try {
      await insertComment(comment.trim())
      revalidatePath('/comments')
    } catch (error) {
      console.error('Error creating comment:', error)
    }
  }

  // Fetch existing comments with error handling
  let comments: any[] = []
  let error: string | null = null
  
  try {
    comments = await getComments()
  } catch (err) {
    console.error('Error fetching comments:', err)
    error = 'Failed to load comments. Database may not be initialized.'
  }

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">Comments</h1>
      
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-yellow-800">
            ⚠️ {error}
          </p>
          <p className="text-yellow-700 text-sm mt-2">
            To initialize the database, visit: <a href="/api/init-db" className="underline">/api/init-db</a>
          </p>
        </div>
      )}
      
      {/* Comment Form */}
      <form action={create} className="mb-8">
        <div className="space-y-4">
          <div>
            <label htmlFor="comment" className="block text-sm font-medium mb-2">
              Add a comment
            </label>
            <textarea
              id="comment"
              name="comment"
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Write your comment here..."
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors"
            disabled={!!error}
          >
            Post Comment
          </button>
        </div>
      </form>

      {/* Comments List */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">
          Comments ({comments.length})
        </h2>
        
        {comments.length === 0 && !error ? (
          <p className="text-gray-500 italic">
            No comments yet. Be the first to comment!
          </p>
        ) : (
          <div className="space-y-4">
            {comments.map((comment: any) => (
              <div
                key={comment.id}
                className="bg-gray-50 p-4 rounded-lg border"
              >
                <p className="text-gray-800 mb-2">{comment.comment}</p>
                <p className="text-sm text-gray-500">
                  {new Date(comment.created_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
