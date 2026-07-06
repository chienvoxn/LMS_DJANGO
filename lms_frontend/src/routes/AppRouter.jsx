import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Register from '../pages/Register';
import CourseDetail from '../pages/CourseDetail';
import CourseLandingPage from '../pages/courses/CourseLandingPage';
import CourseLearning from '../pages/CourseLearning';
import LessonPlayer from '../pages/LessonPlayer';
import StudentDashboard from '../pages/StudentDashboard';
import TeacherDashboard from '../pages/TeacherDashboard';
import CourseEditor from '../pages/CourseEditor';
import TeacherCourseQuizzes from '../pages/TeacherCourseQuizzes';
import QuizEditor from '../pages/QuizEditor';
import StudentQuizPlayer from '../pages/StudentQuizPlayer';
import AssignmentDetail from '../pages/AssignmentDetail';
import StudentAssignmentDetail from '../pages/StudentAssignmentDetail';
import TeacherCourseAssignments from '../pages/TeacherCourseAssignments';
import TeacherAssignmentEditor from '../pages/TeacherAssignmentEditor';
import TeacherAssignmentSubmissions from '../pages/TeacherAssignmentSubmissions';
import TeacherAnalytics from '../pages/TeacherAnalytics';
import TeacherStudents from '../pages/TeacherStudents';
import StudentProfile from '../pages/StudentProfile';
import MyLearning from '../pages/MyLearning';
import PublicProfile from '../pages/profile/PublicProfile';
import EditProfile from '../pages/profile/EditProfile';
import InstructorProfile from '../pages/instructor/InstructorProfile';
import ChangePassword from '../pages/ChangePassword';
import CertificateView from '../pages/CertificateView';
import StudentCertificates from '../pages/StudentCertificates';
import PaymentPage from '../pages/PaymentPage';
import CartPage from '../pages/CartPage';
import CartCheckoutPage from '../pages/CartCheckoutPage';
import StudentPaymentHistory from '../pages/StudentPaymentHistory';
import BrowseCourses from '../pages/BrowseCourses';
import Navbar from '../components/Navbar';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="container">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const TeacherRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="container">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (user?.role !== 'teacher') {
    return <Navigate to="/" replace />;
  }

  return children;
};

const StudentRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="container">Loading...</div>;
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
        <Route path="/" element={<Home />} />
        <Route path="/browse" element={<BrowseCourses />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/student/:studentId/profile" element={<StudentProfile />} />
        {/* User Profile Routes */}
        <Route path="/profile/:userId" element={<PublicProfile />} />
        <Route
          path="/profile/:userId/edit"
          element={
            <ProtectedRoute>
              <EditProfile />
            </ProtectedRoute>
          }
        />
        {/* Instructor Public Profile Route */}
        <Route path="/instructor/:instructorId/profile" element={<InstructorProfile />} />
        {/* Change Password Route */}
        <Route
          path="/account/change-password"
          element={
            <ProtectedRoute>
              <ChangePassword />
            </ProtectedRoute>
          }
        />
        {/* Payment History Route */}
        <Route
          path="/account/payment-history"
          element={
            <StudentRoute>
              <StudentPaymentHistory />
            </StudentRoute>
          }
        />
        <Route path="/courses/:courseId" element={<CourseLandingPage />} />
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
          path="/courses/:courseId/certificate"
          element={
            <ProtectedRoute>
              <CertificateView />
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
          path="/dashboard"
          element={
            <ProtectedRoute>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />
        {/* My Learning */}
        <Route
          path="/my-learning"
          element={
            <StudentRoute>
              <MyLearning />
            </StudentRoute>
          }
        />
        {/* Student Certificates */}
        <Route
          path="/student/certificates"
          element={
            <StudentRoute>
              <StudentCertificates />
            </StudentRoute>
          }
        />
        {/* Cart */}
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
        {/* Teacher Dashboard */}
        <Route
          path="/teacher/dashboard"
          element={
            <TeacherRoute>
              <TeacherDashboard />
            </TeacherRoute>
          }
        />
        {/* Teacher Analytics */}
        <Route
          path="/teacher/analytics"
          element={
            <TeacherRoute>
              <TeacherAnalytics />
            </TeacherRoute>
          }
        />
        {/* Teacher Course Editor */}
        {/* Put /new route BEFORE /:courseId/edit to avoid route conflict */}
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
        {/* Teacher Quiz Management Routes */}
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
        {/* Teacher Assignment Management Routes */}
        <Route
          path="/teacher/courses/:courseId/assignments"
          element={
            <TeacherRoute>
              <TeacherCourseAssignments />
            </TeacherRoute>
          }
        />
        {/* Teacher Student Management Routes */}
        <Route
          path="/teacher/courses/:courseId/students"
          element={
            <TeacherRoute>
              <TeacherStudents />
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
        {/* Student Quiz Player */}
        <Route
          path="/courses/:courseId/quizzes/:quizId/take"
          element={
            <ProtectedRoute>
              <StudentQuizPlayer />
            </ProtectedRoute>
          }
        />
        {/* Student Assignment Detail */}
        <Route
          path="/courses/:courseId/assignments/:assignmentId"
          element={
            <ProtectedRoute>
              <StudentAssignmentDetail />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;

