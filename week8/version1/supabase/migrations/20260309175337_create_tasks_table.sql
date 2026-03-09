/*
  # Create tasks table for pet shop task manager

  1. New Tables
    - `tasks`
      - `id` (uuid, primary key) - Unique identifier for each task
      - `title` (text, required) - The task title
      - `description` (text, optional) - Additional task details
      - `completed` (boolean, default false) - Task completion status
      - `created_at` (timestamptz, default now) - When the task was created

  2. Security
    - Enable RLS on `tasks` table
    - Add public policies for full CRUD access (since no authentication is required)
    - Separate policies for SELECT, INSERT, UPDATE, and DELETE operations
*/

CREATE TABLE IF NOT EXISTS tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text DEFAULT '',
  completed boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view tasks"
  ON tasks FOR SELECT
  USING (true);

CREATE POLICY "Anyone can create tasks"
  ON tasks FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Anyone can update tasks"
  ON tasks FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete tasks"
  ON tasks FOR DELETE
  USING (true);