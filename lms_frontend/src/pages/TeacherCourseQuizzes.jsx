import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { assessmentsAPI, coursesAPI } from '../api/client';

/**
 * TeacherCourseQuizzes Page
 * 
 * Displays all quizzes for a specific course and allows creating new quizzes.
 * Route: /teacher/courses/:courseId/quizzes
 * 
 * Manual Test Steps:
 * 1. Login as teacher
 * 2. Navigate to Teacher Dashboard → choose a course → "Edit"
 * 3. Click "Manage Quizzes" button
 * 4. Create a new quiz
 * 5. Click "Edit" on the quiz to open QuizEditor
 */
const TeacherCourseQuizzes = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [quizzes, setQuizzes] = useState([]);
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [creating, setCreating] = useState(false);

  // Form state for creating quiz
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    time_limit: '',
    is_published: false,
  });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (user?.role !== 'teacher') {
      navigate('/');
      return;
    }

    fetchData();
  }, [courseId, isAuthenticated, user, navigate]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch course info
      try {
        const courseResponse = await coursesAPI.getById(courseId);
        setCourse(courseResponse.data);
      } catch (err) {
        console.error('Error fetching course:', err);
      }

      // Fetch quizzes for this course
      const response = await assessmentsAPI.getTeacherQuizzes({ course: courseId });
      let quizzesData = [];
      if (Array.isArray(response.data)) {
        quizzesData = response.data;
      } else if (response.data?.results) {
        quizzesData = response.data.results;
      }
      // Filter by course if needed (backend should already filter, but just in case)
      setQuizzes(quizzesData.filter(q => q.course === parseInt(courseId) || q.course?.id === parseInt(courseId)));
    } catch (err) {
      console.error('Error fetching quizzes:', err);
      setError(err.response?.data?.detail || 'Failed to load quizzes');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateQuiz = async (e) => {
    e.preventDefault();
    if (!formData.title.trim()) {
      setError('Quiz title is required');
      return;
    }

    setCreating(true);
    setError(null);

    try {
      const quizData = {
        course: parseInt(courseId),
        title: formData.title.trim(),
        description: formData.description.trim(),
        time_limit: formData.time_limit ? parseInt(formData.time_limit) : null,
        is_published: formData.is_published,
      };

      const response = await assessmentsAPI.createTeacherQuiz(quizData);
      setShowCreateForm(false);
      setFormData({ title: '', description: '', time_limit: '', is_published: false });
      
      // Navigate to quiz editor
      navigate(`/teacher/quizzes/${response.data.id}/edit`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create quiz');
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteQuiz = async (quizId) => {
    if (!window.confirm('Are you sure you want to delete this quiz? This action cannot be undone.')) {
      return;
    }

    try {
      await assessmentsAPI.deleteTeacherQuiz(quizId);
      fetchData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete quiz');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 dark:border-primary-400"></div>
          <p className="mt-4 text-slate-600 dark:text-slate-400">Loading quizzes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
        {/* Header - Coursera Style */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
              Quizzes for {course?.title || 'Course'}
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Manage quizzes for this course
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate(`/teacher/courses/${courseId}/edit`)}
              className="px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition"
            >
              Back to Course
            </button>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg text-sm font-medium transition shadow-md hover:shadow-lg"
            >
              {showCreateForm ? 'Cancel' : 'Create New Quiz'}
            </button>
          </div>
        </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-800 dark:text-red-300">
          {error}
          <button
            onClick={() => setError(null)}
            className="ml-4 text-sm underline hover:text-red-900 dark:hover:text-red-400"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Create Quiz Form - Coursera Style */}
      {showCreateForm && (
        <div className="bg-white dark:bg-slate-800 shadow-md rounded-2xl p-6 border-2 border-slate-200 dark:border-slate-700">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-4">Create New Quiz</h2>
          <form onSubmit={handleCreateQuiz} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
                className="w-full px-3 py-2 border-2 border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:border-primary-500 dark:focus:border-primary-400 focus:ring-2 focus:ring-primary-200 dark:focus:ring-primary-900 transition bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
                placeholder="Enter quiz title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 border-2 border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:border-primary-500 dark:focus:border-primary-400 focus:ring-2 focus:ring-primary-200 dark:focus:ring-primary-900 transition bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
                placeholder="Enter quiz description"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Time Limit (minutes)
                </label>
                <input
                  type="number"
                  value={formData.time_limit}
                  onChange={(e) => setFormData({ ...formData, time_limit: e.target.value })}
                  min="1"
                  className="w-full px-3 py-2 border-2 border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:border-primary-500 dark:focus:border-primary-400 focus:ring-2 focus:ring-primary-200 dark:focus:ring-primary-900 transition bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
                  placeholder="Optional"
                />
              </div>

              <div className="flex items-center pt-6">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.is_published}
                    onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                    className="w-4 h-4 text-primary-500 border-slate-300 dark:border-slate-600 rounded focus:ring-primary-500"
                  />
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Publish immediately</span>
                </label>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={creating}
                className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed transition shadow-md hover:shadow-lg"
              >
                {creating ? 'Creating...' : 'Create Quiz'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowCreateForm(false);
                  setFormData({ title: '', description: '', time_limit: '', is_published: false });
                }}
                className="px-4 py-2 text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-600 rounded-lg text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-700 transition"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Quizzes List - Coursera Style */}
      {quizzes.length === 0 ? (
        <div className="bg-white dark:bg-slate-800 shadow-md rounded-2xl p-12 text-center border-2 border-slate-200 dark:border-slate-700">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-2">
            No quizzes yet
          </h3>
          <p className="text-slate-600 dark:text-slate-400 mb-6">
            Create your first quiz to start assessing your students
          </p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition shadow-md hover:shadow-lg"
          >
            Create Your First Quiz
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {quizzes.map((quiz) => (
            <div
              key={quiz.id}
              className="bg-white dark:bg-slate-800 shadow-md rounded-2xl p-6 border-2 border-slate-200 dark:border-slate-700 hover:shadow-lg hover:border-primary-200 dark:hover:border-primary-800 transition"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{quiz.title}</h3>
                    {quiz.is_published ? (
                      <span className="px-2.5 py-1 bg-accent-100 dark:bg-accent-900/30 text-accent-700 dark:text-accent-300 text-xs font-medium rounded-full border border-accent-200 dark:border-accent-800">
                        Published
                      </span>
                    ) : (
                      <span className="px-2.5 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 text-xs font-medium rounded-full border border-yellow-200 dark:border-yellow-800">
                        Draft
                      </span>
                    )}
                  </div>
                  {quiz.description && (
                    <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">{quiz.description}</p>
                  )}
                  <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
                    {quiz.time_limit && (
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {quiz.time_limit} minutes
                      </span>
                    )}
                    <span className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      {quiz.questions_count || 0} questions
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => navigate(`/teacher/quizzes/${quiz.id}/edit`)}
                    className="px-3 py-1.5 bg-primary-500 hover:bg-primary-600 text-white rounded-lg text-sm font-medium transition shadow-sm hover:shadow-md"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteQuiz(quiz.id)}
                    className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition shadow-sm hover:shadow-md"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      </div>
    </div>
  );
};

export default TeacherCourseQuizzes;

