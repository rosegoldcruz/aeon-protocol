import { neon } from '@neondatabase/serverless';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export default async function CommentsPage() {
  // Server Action to create a comment
  async function create(formData: FormData) {
    'use server';
    
    // Connect to the Neon database
    const sql = neon(process.env.DATABASE_URL!);
    const comment = formData.get('comment') as string;
    
    // Validate comment
    if (!comment || comment.trim().length === 0) {
      return;
    }
    
    try {
      // Insert the comment from the form into the Postgres database
      await sql`INSERT INTO comments (comment) VALUES (${comment.trim()})`;
      
      // Revalidate the page to show the new comment
      revalidatePath('/comments');
    } catch (error) {
      console.error('Error creating comment:', error);
    }
  }

  // Fetch existing comments
  async function getComments() {
    const sql = neon(process.env.DATABASE_URL!);
    try {
      const comments = await sql`
        SELECT id, comment, created_at 
        FROM comments 
        ORDER BY created_at DESC
      `;
      return comments;
    } catch (error) {
      console.error('Error fetching comments:', error);
      return [];
    }
  }

  const comments = await getComments();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Comments</h1>
          <p className="text-gray-600">Share your thoughts and see what others are saying</p>
        </div>

        {/* Comment Form */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Add Your Comment</h2>
          <form action={create} className="space-y-4">
            <div>
              <label htmlFor="comment" className="block text-sm font-medium text-gray-700 mb-2">
                Your Comment
              </label>
              <textarea
                id="comment"
                name="comment"
                placeholder="Write your comment here..."
                className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-colors"
                rows={4}
                required
                minLength={1}
                maxLength={1000}
              />
              <p className="text-sm text-gray-500 mt-1">Maximum 1000 characters</p>
            </div>
            <button
              type="submit"
              className="w-full sm:w-auto bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium"
            >
              Submit Comment
            </button>
          </form>
        </div>

        {/* Comments List */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold text-gray-900">
              Recent Comments ({comments.length})
            </h2>
          </div>
          
          {comments.length === 0 ? (
            <div className="text-center py-12">
              <div className="bg-white rounded-xl shadow-sm border p-8">
                <div className="text-gray-400 mb-4">
                  <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No comments yet</h3>
                <p className="text-gray-500">Be the first to share your thoughts!</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {comments.map((comment: any, index: number) => (
                <div key={comment.id} className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-blue-600 font-medium text-sm">
                          {index + 1}
                        </span>
                      </div>
                      <span className="text-sm text-gray-500">
                        Comment #{comment.id}
                      </span>
                    </div>
                    <time className="text-sm text-gray-500">
                      {new Date(comment.created_at).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </time>
                  </div>
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                    {comment.comment}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Back to Dashboard */}
        <div className="mt-8 text-center">
          <a
            href="/dashboard"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Dashboard
          </a>
        </div>
      </div>
    </div>
  );
}
