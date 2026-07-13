import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';

import Home from '../pages/Home';
import Login from '../pages/Login';
import Register from '../pages/Register';

import BrowseCourses from '../pages/BrowseCourses';
import CourseLandingPage from '../pages/courses/CourseLandingPage';
import CourseLearning from '../pages/CourseLearning';
import LessonPlayer from '../pages/LessonPlayer';

import StudentDashboard from '../pages/StudentDashboard';
import MyLearning from '../pages/MyLearning';
import StudentProfile from '../pages/StudentProfile';
import StudentCertificates from '../pages/StudentCertificates';
import StudentPaymentHistory from '../pages/StudentPaymentHistory';

import TeacherDashboard from '../pages/TeacherDashboard';
import TeacherAnalytics from '../pages/TeacherAnalytics';
import TeacherStudents from '../pages/TeacherStudents';
import CourseEditor from '../pages/CourseEditor';

import TeacherCourseQuizzes from '../pages/TeacherCourseQuizzes';
import QuizEditor from '../pages/QuizEditor';
import StudentQuizPlayer from '../pages/StudentQuizPlayer';

import TeacherCourseAssignments from '../pages/TeacherCourseAssignments';
import TeacherAssignmentEditor from '../pages/TeacherAssignmentEditor';
import TeacherAssignmentSubmissions from '../pages/TeacherAssignmentSubmissions';
import StudentAssignmentDetail from '../pages/StudentAssignmentDetail';

import PublicProfile from '../pages/profile/PublicProfile';
import EditProfile from '../pages/profile/EditProfile';
import InstructorProfile from '../pages/instructor/InstructorProfile';

import ChangePassword from '../pages/ChangePassword';
import CertificateView from '../pages/CertificateView';

import PaymentPage from '../pages/PaymentPage';
import CartPage from '../pages/CartPage';
import CartCheckoutPage from '../pages/CartCheckoutPage';

import ChatPage from '../pages/ChatPage';
import AIAssistant from '../pages/AIAssistant';

import Navbar from '../components/Navbar';

/**
 * Route dành cho mọi người dùng đã đăng nhập.
 * Student và teacher đều có thể truy cập.
 */
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-10">
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

/**
 * Route chỉ dành cho giảng viên.
 */
const TeacherRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-10">
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (user?.role !== 'teacher') {
    return <Navigate to="/" replace />;
  }

  return children;
};

/**
 * Route chỉ dành cho học viên.
 */
const StudentRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-10">
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (user?.role !== 'student') {
    return <Navigate to="/" replace />;
  }

  return children;
};

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Home />} />
        <Route path="/browse" element={<BrowseCourses />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Public profile routes */}
        <Route
          path="/student/:studentId/profile"
          element={<StudentProfile />}
        />

        <Route
          path="/profile/:userId"
          element={<PublicProfile />}
        />

        <Route
          path="/instructor/:instructorId/profile"
          element={<InstructorProfile />}
        />

        {/* Protected user profile routes */}
        <Route
          path="/profile/:userId/edit"
          element={
            <ProtectedRoute>
              <EditProfile />
            </ProtectedRoute>
          }
        />

        <Route
          path="/account/change-password"
          element={
            <ProtectedRoute>
              <ChangePassword />
            </ProtectedRoute>
          }
        />

        {/* Course routes */}
        <Route
          path="/courses/:courseId"
          element={<CourseLandingPage />}
        />

        <Route
          path="/courses/:courseId/payment"
          element={
            <ProtectedRoute>
              <PaymentPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/courses/:courseId/learn"
          element={
            <ProtectedRoute>
              <CourseLearning />
            </ProtectedRoute>
          }
        />

        <Route
          path="/courses/:courseId/lessons/:lessonId"
          element={
            <ProtectedRoute>
              <LessonPlayer />
            </ProtectedRoute>
          }
        />

        <Route
          path="/courses/:courseId/certificate"
          element={
            <ProtectedRoute>
              <CertificateView />
            </ProtectedRoute>
          }
        />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />

        {/* AI Assistant */}
        <Route
          path="/ai-assistant"
          element={
            <ProtectedRoute>
              <AIAssistant />
            </ProtectedRoute>
          }
        />

        {/* Chat */}
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />

        {/* Student routes */}
        <Route
          path="/my-learning"
          element={
            <StudentRoute>
              <MyLearning />
            </StudentRoute>
          }
        />

        <Route
          path="/student/certificates"
          element={
            <StudentRoute>
              <StudentCertificates />
            </StudentRoute>
          }
        />

        <Route
          path="/account/payment-history"
          element={
            <StudentRoute>
              <StudentPaymentHistory />
            </StudentRoute>
          }
        />

        {/* Cart routes */}
        <Route
          path="/cart"
          element={
            <ProtectedRoute>
              <CartPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/cart/checkout"
          element={
            <ProtectedRoute>
              <CartCheckoutPage />
            </ProtectedRoute>
          }
        />

        {/* Student quiz */}
        <Route
          path="/courses/:courseId/quizzes/:quizId/take"
          element={
            <ProtectedRoute>
              <StudentQuizPlayer />
            </ProtectedRoute>
          }
        />

        {/* Student assignment */}
        <Route
          path="/courses/:courseId/assignments/:assignmentId"
          element={
            <ProtectedRoute>
              <StudentAssignmentDetail />
            </ProtectedRoute>
          }
        />

        {/* Teacher dashboard */}
        <Route
          path="/teacher/dashboard"
          element={
            <TeacherRoute>
              <TeacherDashboard />
            </TeacherRoute>
          }
        />

        {/* Teacher analytics */}
        <Route
          path="/teacher/analytics"
          element={
            <TeacherRoute>
              <TeacherAnalytics />
            </TeacherRoute>
          }
        />

        {/* Teacher course management */}
        <Route
          path="/teacher/courses/new"
          element={
            <TeacherRoute>
              <CourseEditor />
            </TeacherRoute>
          }
        />

        <Route
          path="/teacher/courses/:courseId/edit"
          element={
            <TeacherRoute>
              <CourseEditor />
            </TeacherRoute>
          }
        />

        {/* Teacher quiz management */}
        <Route
          path="/teacher/courses/:courseId/quizzes"
          element={
            <TeacherRoute>
              <TeacherCourseQuizzes />
            </TeacherRoute>
          }
        />

        <Route
          path="/teacher/quizzes/:quizId/edit"
          element={
            <TeacherRoute>
              <QuizEditor />
            </TeacherRoute>
          }
        />

        {/* Teacher assignment management */}
        <Route
          path="/teacher/courses/:courseId/assignments"
          element={
            <TeacherRoute>
              <TeacherCourseAssignments />
            </TeacherRoute>
          }
        />

        <Route
          path="/teacher/assignments/:assignmentId/edit"
          element={
            <TeacherRoute>
              <TeacherAssignmentEditor />
            </TeacherRoute>
          }
        />

        <Route
          path="/teacher/assignments/:assignmentId/submissions"
          element={
            <TeacherRoute>
              <TeacherAssignmentSubmissions />
            </TeacherRoute>
          }
        />

        {/* Teacher student management */}
        <Route
          path="/teacher/courses/:courseId/students"
          element={
            <TeacherRoute>
              <TeacherStudents />
            </TeacherRoute>
          }
        />

        {/* Fallback route */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;