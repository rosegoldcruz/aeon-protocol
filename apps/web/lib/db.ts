import { neon } from '@neondatabase/serverless';

// Initialize Neon database connection
export const sql = neon(process.env['DATABASE_URL']!);

// Create comments table if it doesn't exist
export async function initializeDatabase() {
  try {
    await sql`
      CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
}

// Get all comments
export async function getComments() {
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

// Insert a new comment
export async function insertComment(comment: string) {
  try {
    const result = await sql`
      INSERT INTO comments (comment) 
      VALUES (${comment}) 
      RETURNING id, comment, created_at
    `;
    return result[0];
  } catch (error) {
    console.error('Error inserting comment:', error);
    throw error;
  }
}
