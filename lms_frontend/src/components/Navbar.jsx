import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import { useState, useEffect, useRef } from "react";
import { getCart } from "../api/client";

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showChatDialog, setShowChatDialog] = useState(false);
  const [cartCount, setCartCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState("");
  const dropdownRef = useRef(null);
  const chatRef = useRef(null);

  const handleLogout = () => {
    logout();
    navigate("/");
    setShowDropdown(false);
  };

  const handleViewProfile = () => {
    if (user?.id) {
      if (user?.role === "teacher") {
        navigate(`/instructor/${user.id}/profile`);
      } else {
        navigate(`/profile/${user.id}`);
      }
      setShowDropdown(false);
    }
  };

  // Fetch cart count for students
  useEffect(() => {
    if (isAuthenticated && user?.role === "student") {
      const fetchCartCount = async () => {
        try {
          const response = await getCart();
          setCartCount(response.data.count || 0);
        } catch (err) {
          setCartCount(0);
        }
      };
      fetchCartCount();
    } else {
      setCartCount(0);
    }
  }, [isAuthenticated, user, location.pathname]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
      if (chatRef.current && !chatRef.current.contains(event.target)) {
        setShowChatDialog(false);
      }
    };

    if (showDropdown || showChatDialog) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showDropdown, showChatDialog]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/browse?search=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery("");
    } else {
      navigate("/browse");
    }
  };

  const getAvatarUrl = (user) => {
    if (user?.avatar_url) {
      return user.avatar_url;
    }
    const name = user?.full_name || user?.email || "U";
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=6366f1&color=fff&size=128`;
  };

  return (
    <nav className="bg-white dark:bg-slate-800 shadow-sm sticky top-0 z-50 border-b border-slate-100 dark:border-slate-700 transition-colors">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between gap-6">
        {/* Logo - Coursera style */}
        <Link
          to="/"
          className="text-2xl font-bold text-primary-500 hover:text-primary-600 dark:text-primary-400 dark:hover:text-primary-300 transition-colors flex-shrink-0"
        >
          LMS
        </Link>

        {/* Navigation Links - Center Left */}
        <div className="hidden lg:flex items-center gap-6 flex-1">
          {isAuthenticated && user?.role === "student" && (
            <>
              <Link
                to="/browse"
                className="text-slate-700 hover:text-primary-500 dark:text-slate-300 dark:hover:text-primary-400 font-medium text-sm transition-colors"
              >
                Browse
              </Link>
              <Link
                to="/my-learning"
                className="text-slate-700 hover:text-primary-500 dark:text-slate-300 dark:hover:text-primary-400 font-medium text-sm transition-colors"
              >
                My Learning
              </Link>
            </>
          )}
        </div>

        {/* Search Bar - Center (Coursera style) */}
        {isAuthenticated && user?.role === "student" && (
          <form
            onSubmit={handleSearch}
            className="hidden md:flex flex-1 max-w-xl mx-4"
          >
            <div className="w-full bg-slate-50 dark:bg-slate-700 rounded-full px-6 py-3 flex items-center gap-3 border border-slate-200 dark:border-slate-600 hover:border-slate-300 dark:hover:border-slate-500 focus-within:border-primary-400 dark:focus-within:border-primary-400 focus-within:ring-2 focus-within:ring-primary-100 dark:focus-within:ring-primary-900 transition-all duration-200">
              <input
                type="text"
                placeholder="What do you want to learn?"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 bg-transparent text-slate-900 dark:text-slate-100 placeholder-slate-500 dark:placeholder-slate-400 outline-none text-sm"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery("")}
                  className="text-slate-400 hover:text-slate-600 dark:text-slate-400 dark:hover:text-slate-300 transition-colors p-1"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              )}
              <button
                type="submit"
                className="bg-primary-500 hover:bg-primary-600 text-white rounded-full p-2 transition-colors"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </button>
            </div>
          </form>
        )}

        {/* Right Side Actions */}
        <div className="flex items-center gap-4 flex-shrink-0">
          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-slate-700 hover:text-primary-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-primary-400 dark:hover:bg-slate-700 transition-colors"
            aria-label={
              theme === "light" ? "Switch to dark mode" : "Switch to light mode"
            }
          >
            {theme === "light" ? (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                />
              </svg>
            ) : (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 3v1m0 16v1m8.66-11.66l-.71.71M5.05 18.95l-.71.71M18.36 5.64l-.71-.71M5.05 5.05l.71.71M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                />
              </svg>
            )}
          </button>

          {!isAuthenticated ? (
            <>
              <Link
                to="/login"
                className="text-slate-700 hover:text-primary-500 dark:text-slate-300 dark:hover:text-primary-400 font-medium text-sm transition-colors"
              >
                Log In
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-full transition-colors text-sm font-semibold"
              >
                Join for Free
              </Link>
            </>
          ) : (
            <>
              {user?.role === "teacher" && (
                <>
                  <Link
                    to="/teacher/dashboard"
                    className="text-slate-700 hover:text-primary-500 dark:text-slate-300 dark:hover:text-primary-400 font-medium text-sm transition-colors"
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/teacher/analytics"
                    className="text-slate-700 hover:text-primary-500 dark:text-slate-300 dark:hover:text-primary-400 font-medium text-sm transition-colors"
                  >
                    Analytics
                  </Link>
                </>
              )}
              {user?.role === "student" && (
                <Link
                  to="/cart"
                  className="relative text-slate-700 hover:text-primary-500 dark:text-slate-300 dark:hover:text-primary-400 transition-colors"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                    />
                  </svg>
                  {cartCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-primary-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                      {cartCount > 9 ? "9+" : cartCount}
                    </span>
                  )}
                </Link>
              )}

              {/* Chat Button - Authenticated users */}
              <div className="relative" ref={chatRef}>
                <button
                  onClick={() => setShowChatDialog(!showChatDialog)}
                  className="p-2 rounded-lg text-slate-700 hover:text-primary-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-primary-400 dark:hover:bg-slate-700 transition-colors relative"
                  aria-label="Open chat"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"
                    />
                  </svg>
                  <span className="absolute top-1 right-1 w-2 h-2 bg-green-500 rounded-full ring-2 ring-white dark:ring-slate-800"></span>
                </button>

                {/* Chat Dialog Placeholder */}
                {showChatDialog && (
                  <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-slate-800 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 py-2 z-50">
                    <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
                      <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                        Chat hỗ trợ
                      </p>
                      <p className="text-xs text-slate-500 dark:text-slate-400">
                        Chúng tôi sẽ hỗ trợ bạn
                      </p>
                    </div>
                    <div className="px-4 py-6 text-center text-slate-500 dark:text-slate-400 text-sm min-h-[200px] flex items-center justify-center">
                      Hộp thoại chat sẽ được bổ sung sau
                    </div>
                  </div>
                )}
              </div>

              {/* User Menu Dropdown */}
              <div className="relative" ref={dropdownRef}>
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="flex items-center gap-2 hover:opacity-80 transition"
                >
                  <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold text-sm">
                    {user?.full_name?.[0]?.toUpperCase() ||
                      user?.email?.[0]?.toUpperCase() ||
                      "U"}
                  </div>
                </button>

                {/* Dropdown Menu */}
                {showDropdown && (
                  <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-slate-800 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 py-2 z-50">
                    {/* User Info Section */}
                    <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
                      <div className="flex items-center gap-3">
                        <img
                          src={getAvatarUrl(user)}
                          alt={user?.full_name || user?.email}
                          className="w-10 h-10 rounded-full object-cover"
                          onError={(e) => {
                            e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.full_name?.[0] || user?.email?.[0] || "U")}&background=6366f1&color=fff&size=128`;
                          }}
                        />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
                            {user?.full_name || "No name"}
                          </p>
                          <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
                            {user?.email}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Menu Items */}
                    <div className="py-1">
                      <button
                        onClick={handleViewProfile}
                        className="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition flex items-center gap-3"
                      >
                        <svg
                          className="w-5 h-5 text-slate-500 dark:text-slate-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                          />
                        </svg>
                        View Profile
                      </button>
                      {user?.role === "student" && (
                        <>
                          <button
                            onClick={() => {
                              navigate("/student/certificates");
                              setShowDropdown(false);
                            }}
                            className="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition flex items-center gap-3"
                          >
                            <svg
                              className="w-5 h-5 text-slate-500 dark:text-slate-400"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                              />
                            </svg>
                            View all certificates
                          </button>
                          <button
                            onClick={() => {
                              navigate("/account/payment-history");
                              setShowDropdown(false);
                            }}
                            className="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition flex items-center gap-3"
                          >
                            <svg
                              className="w-5 h-5 text-slate-500 dark:text-slate-400"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                              />
                            </svg>
                            Payment history
                          </button>
                        </>
                      )}
                      <button
                        onClick={() => {
                          navigate("/account/change-password");
                          setShowDropdown(false);
                        }}
                        className="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition flex items-center gap-3"
                      >
                        <svg
                          className="w-5 h-5 text-slate-500 dark:text-slate-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                          />
                        </svg>
                        Change Password
                      </button>
                    </div>

                    {/* Divider */}
                    <div className="border-t border-slate-200 dark:border-slate-700 my-1"></div>

                    {/* Logout */}
                    <div className="py-1">
                      <button
                        onClick={handleLogout}
                        className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition flex items-center gap-3"
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                          />
                        </svg>
                        Logout
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
