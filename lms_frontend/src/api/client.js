import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // If data is FormData, don't set Content-Type (let browser set it with boundary)
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
          const response = await axios.post(
            'http://localhost:8000/api/auth/refresh/',
            { refresh: refreshToken }
          );
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Helper methods
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  me: () => api.get('/auth/me/'),
  refresh: (refreshToken) => api.post('/auth/refresh/', { refresh: refreshToken }),
  changePassword: (payload) => api.post('/auth/change-password/', payload),
};

export const coursesAPI = {
  getAll: (params) => api.get('/courses/', { params }),
  getById: (id) => api.get(`/courses/${id}/`),
  getCurriculum: (id) => api.get(`/courses/${id}/curriculum/`),
  // Teacher course management
  getTeacherCourses: (params) => api.get('/teacher/courses/', { params }),
  createTeacherCourse: (data) => api.post('/teacher/courses/', data),
  getTeacherCourseDetail: (id) => api.get(`/teacher/courses/${id}/`),
  updateTeacherCourse: (id, data) => api.patch(`/teacher/courses/${id}/`, data),
  deleteTeacherCourse: (id) => api.delete(`/teacher/courses/${id}/`),
  // Teacher section management
  getTeacherSections: (params) => api.get('/teacher/sections/', { params }),
  createTeacherSection: (data) => api.post('/teacher/sections/', data),
  updateTeacherSection: (id, data) => api.patch(`/teacher/sections/${id}/`, data),
  deleteTeacherSection: (id) => api.delete(`/teacher/sections/${id}/`),
  // Teacher lesson management
  getTeacherLessons: (params) => api.get('/teacher/lessons/', { params }),
  createTeacherLesson: (data) => api.post('/teacher/lessons/', data),
  updateTeacherLesson: (id, data) => api.patch(`/teacher/lessons/${id}/`, data),
  deleteTeacherLesson: (id) => api.delete(`/teacher/lessons/${id}/`),
};

export const enrollmentsAPI = {
  enroll: (courseId) => api.post(`/courses/${courseId}/enroll/`),
  getMyEnrollments: () => api.get('/enrollments/me/'),
  completeLesson: (lessonId) => api.post(`/lessons/${lessonId}/complete/`),
};

export const lessonsAPI = {
  getById: (id) => api.get(`/lessons/${id}/`),
};

// Teacher Quiz & Assignment APIs
export const assessmentsAPI = {
  // Quiz management
  getTeacherQuizzes: (params) => api.get('/teacher/quizzes/', { params }),
  createTeacherQuiz: (data) => api.post('/teacher/quizzes/', data),
  getTeacherQuizDetail: (id) => api.get(`/teacher/quizzes/${id}/`),
  updateTeacherQuiz: (id, data) => api.patch(`/teacher/quizzes/${id}/`, data),
  deleteTeacherQuiz: (id) => api.delete(`/teacher/quizzes/${id}/`),
  
  // Question management
  createQuestion: (quizId, data) => api.post(`/teacher/quizzes/${quizId}/questions/`, data),
  updateQuestion: (questionId, data) => api.patch(`/teacher/questions/${questionId}/`, data),
  deleteQuestion: (questionId) => api.delete(`/teacher/questions/${questionId}/`),
  
  // Choice management
  createChoice: (questionId, data) => api.post(`/teacher/questions/${questionId}/choices/`, data),
  updateChoice: (choiceId, data) => api.patch(`/teacher/choices/${choiceId}/`, data),
  deleteChoice: (choiceId) => api.delete(`/teacher/choices/${choiceId}/`),
  
  // Assignment management
  getTeacherAssignments: (params) => api.get('/teacher/assignments/', { params }),
  createTeacherAssignment: (data) => api.post('/teacher/assignments/', data),
  getTeacherAssignmentDetail: (id) => api.get(`/teacher/assignments/${id}/`),
  updateTeacherAssignment: (id, data) => api.patch(`/teacher/assignments/${id}/`, data),
  deleteTeacherAssignment: (id) => api.delete(`/teacher/assignments/${id}/`),
  getAssignmentSubmissions: (id) => api.get(`/teacher/assignments/${id}/submissions/`),
  gradeSubmission: (id, data) => api.patch(`/teacher/submissions/${id}/grade/`, data),
  // File upload
  uploadFile: (formData) => {
    return api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

// Student Quiz APIs
export const studentQuizAPI = {
  getCourseQuizzes: (courseId) => api.get(`/courses/${courseId}/quizzes/`),
  getQuizDetail: (quizId) => api.get(`/quizzes/${quizId}/`),
  startQuiz: (quizId) => api.post(`/quizzes/${quizId}/start/`),
  submitQuiz: (quizId, payload) => api.post(`/quizzes/${quizId}/submit/`, payload),
  getMyQuizAttempt: (quizId) => api.get(`/quizzes/${quizId}/attempts/me/`),
};

// Student Assignment APIs
export const studentAssignmentAPI = {
  getCourseAssignments: (courseId) => api.get(`/courses/${courseId}/assignments/`),
  getAssignmentDetail: (id) => api.get(`/assignments/${id}/`),
  getMySubmission: async (id) => {
    try {
      return await api.get(`/assignments/${id}/my-submission/`);
    } catch (error) {
      // 404 is expected when no submission exists yet
      if (error.response?.status === 404) {
        return { data: null };
      }
      throw error;
    }
  },
  submitAssignment: (id, payload) => {
    // Handle both JSON and FormData
    if (payload instanceof FormData) {
      return api.post(`/assignments/${id}/submit/`, payload, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    }
    return api.post(`/assignments/${id}/submit/`, payload);
  },
  // Helper method for text-only submission
  submitAssignmentText: (id, content) => {
    return api.post(`/assignments/${id}/submit/`, { content });
  },
};

// Student Progress APIs
export const studentProgressAPI = {
  getMyCourses: () => api.get('/student/my-courses/'),
};

// Course Reviews APIs
export const reviewsAPI = {
  getCourseRatingSummary: (courseId) => api.get(`/courses/${courseId}/rating-summary/`),
  getCourseReviews: (courseId) => api.get(`/courses/${courseId}/reviews/`),
  getMyCourseReview: async (courseId) => {
    try {
      return await api.get(`/courses/${courseId}/my-review/`);
    } catch (error) {
      // 404 is expected when no review exists yet - return null data
      if (error.response?.status === 404) {
        return { data: null };
      }
      // Re-throw other errors
      throw error;
    }
  },
  upsertCourseReview: (courseId, data) => api.post(`/courses/${courseId}/reviews/`, data),
  deleteCourseReview: (reviewId) => api.delete(`/reviews/${reviewId}/`),
};

// Purchase API
export const purchaseCourse = (courseId, mode = "paid") =>
  api.post(`/courses/${courseId}/purchase/`, { mode });

// Certificate APIs
export const issueCertificate = (courseId) =>
  api.post(`/courses/${courseId}/certificate/issue/`);

export const getMyCertificateForCourse = (courseId) =>
  api.get(`/courses/${courseId}/certificate/me/`);

export const getMyCertificates = () =>
  api.get("/enrollments/me/certificates/");

// Payment History API
export const getPaymentHistory = () =>
  api.get("/enrollments/me/payments/");

// Teacher Analytics APIs
export const getTeacherSummary = () => api.get("/teacher/analytics/summary/");
export const getTeacherCourseStats = () => api.get("/teacher/analytics/courses/");
export const getTeacherEngagement = () => api.get("/teacher/analytics/engagement/");

// Public APIs for Home Page
export const getCourseCategories = () => api.get("/courses/categories/");
export const getTopInstructors = (sort = 'students') => api.get(`/instructors/top/?sort=${sort}`);
export const getTeacherTimeseries = (months = 6) =>
  api.get("/teacher/analytics/timeseries/", { params: { months } });

// Teacher Course Student Management APIs
export const getCourseStudents = (courseId, params = {}) =>
  api.get(`/teacher/courses/${courseId}/students/`, { params });

export const removeCourseStudent = (courseId, studentId) =>
  api.delete(`/teacher/courses/${courseId}/students/${studentId}/`);

// Student Public Profile API
export const getStudentProfile = (id) => api.get(`/students/${id}/profile/`);

// User Profile APIs
export const getUserProfile = (userId) => api.get(`/users/${userId}/profile/`);
export const getMyProfile = () => api.get(`/users/me/profile/`);
export const updateMyProfile = (data) => api.patch(`/users/me/profile/`, data);
export const putMyProfile = (data) => api.put(`/users/me/profile/`, data);

// Instructor Public Profile API
export const getInstructorProfile = (id) => api.get(`/users/instructors/${id}/profile/`);

// Cart APIs
export const getCart = () => api.get("/enrollments/cart/");
export const addToCart = (courseId) => api.post("/enrollments/cart/add/", { course_id: courseId });
export const removeCartItem = (itemId) => api.delete(`/enrollments/cart/items/${itemId}/`);
export const checkoutCart = (itemIds = null) => {
  const payload = itemIds ? { item_ids: itemIds } : {};
  return api.post("/enrollments/cart/checkout/", payload);
};

export default api;

