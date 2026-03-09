import { useEffect, useState } from 'react';
// import { supabase, Task } from './lib/supabase';
import {
    PawPrint,
    Plus,
    Trash2,
    CreditCard as Edit2,
    Check,
    X,
} from 'lucide-react';

type Task = {
    id: string;
    title: string;
    description: string;
    completed: boolean;
};

function App() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [newTaskDescription, setNewTaskDescription] = useState('');
    const [editingTask, setEditingTask] = useState<Task | null>(null);
    const [editTitle, setEditTitle] = useState('');
    const [editDescription, setEditDescription] = useState('');

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = () => {
        const savedTasks = localStorage.getItem('tasks');

        if (savedTasks) {
            setTasks(JSON.parse(savedTasks));
        } else {
            setTasks([]);
        }
    };

    const addTask = (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTaskTitle.trim()) return;

        const newTask: Task = {
            id: Date.now().toString(),
            title: newTaskTitle,
            description: newTaskDescription,
            completed: false,
        };

        const updatedTasks = [newTask, ...tasks];
        setTasks(updatedTasks);
        localStorage.setItem('tasks', JSON.stringify(updatedTasks));

        setNewTaskTitle('');
        setNewTaskDescription('');
    };

    const toggleComplete = (task: Task) => {
        const updatedTasks = tasks.map((t) =>
            t.id === task.id ? { ...t, completed: !t.completed } : t,
        );

        setTasks(updatedTasks);
        localStorage.setItem('tasks', JSON.stringify(updatedTasks));
    };

    const deleteTask = (taskId: string) => {
        const updatedTasks = tasks.filter((t) => t.id !== taskId);
        setTasks(updatedTasks);
        localStorage.setItem('tasks', JSON.stringify(updatedTasks));
    };

    const startEditing = (task: Task) => {
        setEditingTask(task);
        setEditTitle(task.title);
        setEditDescription(task.description);
    };

    const cancelEditing = () => {
        setEditingTask(null);
        setEditTitle('');
        setEditDescription('');
    };

    const saveEdit = () => {
        if (!editingTask || !editTitle.trim()) return;

        const updatedTasks = tasks.map((t) =>
            t.id === editingTask.id
                ? { ...t, title: editTitle, description: editDescription }
                : t,
        );

        setTasks(updatedTasks);
        localStorage.setItem('tasks', JSON.stringify(updatedTasks));

        cancelEditing();
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-blue-50">
            <div className="max-w-4xl mx-auto px-4 py-8">
                <div className="text-center mb-8">
                    <div className="flex items-center justify-center gap-3 mb-2">
                        <PawPrint className="w-10 h-10 text-orange-500" />
                        <h1 className="text-5xl font-bold bg-gradient-to-r from-orange-500 via-pink-500 to-blue-500 bg-clip-text text-transparent">
                            Paw Market Tasks
                        </h1>
                        <PawPrint className="w-10 h-10 text-pink-500" />
                    </div>
                    <p className="text-gray-600 text-lg">
                        Manage your pet shop adventures!
                    </p>
                </div>

                <div className="bg-white rounded-3xl shadow-lg p-6 mb-8 border-4 border-orange-200">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <Plus className="w-6 h-6 text-orange-500" />
                        Add New Task
                    </h2>
                    <form onSubmit={addTask} className="space-y-4">
                        <div>
                            <input
                                type="text"
                                placeholder="What needs to be done? (e.g., Feed the puppies)"
                                value={newTaskTitle}
                                onChange={(e) =>
                                    setNewTaskTitle(e.target.value)
                                }
                                className="w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition-colors"
                            />
                        </div>
                        <div>
                            <textarea
                                placeholder="Add details... (optional)"
                                value={newTaskDescription}
                                onChange={(e) =>
                                    setNewTaskDescription(e.target.value)
                                }
                                className="w-full px-4 py-3 border-2 border-pink-200 rounded-xl focus:outline-none focus:border-pink-400 transition-colors resize-none"
                                rows={3}
                            />
                        </div>
                        <button
                            type="submit"
                            className="w-full bg-gradient-to-r from-orange-400 to-pink-400 text-white font-semibold py-3 px-6 rounded-xl hover:from-orange-500 hover:to-pink-500 transition-all transform hover:scale-105 shadow-md"
                        >
                            Add Task
                        </button>
                    </form>
                </div>

                <div className="space-y-4">
                    {tasks.length === 0 ? (
                        <div className="bg-white rounded-3xl shadow-lg p-12 text-center border-4 border-blue-200">
                            <PawPrint className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                            <p className="text-gray-500 text-lg">
                                No tasks yet! Add one above to get started.
                            </p>
                        </div>
                    ) : (
                        tasks.map((task) => (
                            <div
                                key={task.id}
                                className={`bg-white rounded-2xl shadow-md p-5 border-4 transition-all hover:shadow-lg ${
                                    task.completed
                                        ? 'border-green-200 bg-green-50'
                                        : 'border-blue-200'
                                }`}
                            >
                                {editingTask?.id === task.id ? (
                                    <div className="space-y-3">
                                        <input
                                            type="text"
                                            value={editTitle}
                                            onChange={(e) =>
                                                setEditTitle(e.target.value)
                                            }
                                            className="w-full px-4 py-2 border-2 border-pink-200 rounded-lg focus:outline-none focus:border-pink-400"
                                        />
                                        <textarea
                                            value={editDescription}
                                            onChange={(e) =>
                                                setEditDescription(
                                                    e.target.value,
                                                )
                                            }
                                            className="w-full px-4 py-2 border-2 border-pink-200 rounded-lg focus:outline-none focus:border-pink-400 resize-none"
                                            rows={2}
                                        />
                                        <div className="flex gap-2">
                                            <button
                                                onClick={saveEdit}
                                                className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                                            >
                                                <Check className="w-4 h-4" />
                                                Save
                                            </button>
                                            <button
                                                onClick={cancelEditing}
                                                className="flex items-center gap-2 px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition-colors"
                                            >
                                                <X className="w-4 h-4" />
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="flex items-start gap-4">
                                        <button
                                            onClick={() => toggleComplete(task)}
                                            className={`flex-shrink-0 w-6 h-6 rounded-full border-3 transition-all mt-1 ${
                                                task.completed
                                                    ? 'bg-green-500 border-green-600'
                                                    : 'border-gray-300 hover:border-pink-400'
                                            }`}
                                        >
                                            {task.completed && (
                                                <Check className="w-full h-full text-white p-0.5" />
                                            )}
                                        </button>
                                        <div className="flex-1">
                                            <h3
                                                className={`text-lg font-semibold mb-1 ${
                                                    task.completed
                                                        ? 'line-through text-gray-500'
                                                        : 'text-gray-800'
                                                }`}
                                            >
                                                {task.title}
                                            </h3>
                                            {task.description && (
                                                <p
                                                    className={`text-sm ${
                                                        task.completed
                                                            ? 'text-gray-400'
                                                            : 'text-gray-600'
                                                    }`}
                                                >
                                                    {task.description}
                                                </p>
                                            )}
                                        </div>
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() =>
                                                    startEditing(task)
                                                }
                                                className="p-2 text-blue-500 hover:bg-blue-100 rounded-lg transition-colors"
                                                title="Edit task"
                                            >
                                                <Edit2 className="w-5 h-5" />
                                            </button>
                                            <button
                                                onClick={() =>
                                                    deleteTask(task.id)
                                                }
                                                className="p-2 text-red-500 hover:bg-red-100 rounded-lg transition-colors"
                                                title="Delete task"
                                            >
                                                <Trash2 className="w-5 h-5" />
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))
                    )}
                </div>

                <div className="mt-8 text-center">
                    <div className="flex items-center justify-center gap-2 text-gray-500">
                        <PawPrint className="w-4 h-4" />
                        <span className="text-sm">
                            {tasks.filter((t) => t.completed).length} of{' '}
                            {tasks.length} tasks completed
                        </span>
                        <PawPrint className="w-4 h-4" />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
