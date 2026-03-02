// frontend/src/components/layout/Sidebar.jsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  BookOpen, 
  ClipboardList, 
  CreditCard, 
  MessageSquare,
  BarChart3,
  Settings,
  LogOut
} from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/slices/authSlice';

const menuItems = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: LayoutDashboard,
    roles: ['admin', 'teacher', 'student', 'parent', 'staff'],
  },
  {
    name: 'Utilisateurs',
    path: '/users',
    icon: Users,
    roles: ['admin'],
  },
  {
    name: 'Académique',
    path: '/academics',
    icon: BookOpen,
    roles: ['admin', 'teacher'],
    children: [
      { name: 'Matières', path: '/academics/subjects' },
      { name: 'Classes', path: '/academics/classes' },
      { name: 'Emploi du temps', path: '/academics/timetable' },
      { name: 'Salles', path: '/academics/classrooms' },
    ],
  },
  {
    name: 'Évaluation',
    path: '/assessment',
    icon: ClipboardList,
    roles: ['admin', 'teacher', 'student', 'parent'],
    children: [
      { name: 'Notes', path: '/assessment/grades' },
      { name: 'Bulletins', path: '/assessment/reports' },
      { name: 'Présence', path: '/assessment/attendance' },
    ],
  },
  {
    name: 'Finances',
    path: '/finance',
    icon: CreditCard,
    roles: ['admin', 'staff'],
    children: [
      { name: 'Paiements', path: '/finance/payments' },
      { name: 'Factures', path: '/finance/invoices' },
    ],
  },
  {
    name: 'Communication',
    path: '/communication',
    icon: MessageSquare,
    roles: ['admin', 'teacher', 'parent'],
    children: [
      { name: 'Messagerie', path: '/communication/messaging' },
      { name: 'Notifications', path: '/communication/notifications' },
    ],
  },
  {
    name: 'Analytiques',
    path: '/analytics',
    icon: BarChart3,
    roles: ['admin'],
  },
  {
    name: 'Paramètres',
    path: '/settings',
    icon: Settings,
    roles: ['admin', 'teacher', 'student', 'parent', 'staff'],
  },
];

const Sidebar = () => {
  const location = useLocation();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const [openSubmenus, setOpenSubmenus] = React.useState({});

  const toggleSubmenu = (path) => {
    setOpenSubmenus((prev) => ({
      ...prev,
      [path]: !prev[path],
    }));
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  const filteredMenuItems = menuItems.filter((item) =>
    item.roles.includes(user?.user_type)
  );

  return (
    <div className="w-64 bg-white shadow-lg h-screen fixed left-0 top-0 overflow-y-auto">
      <div className="p-6 border-b">
        <h1 className="text-xl font-bold text-gray-800">EduERP</h1>
        <p className="text-sm text-gray-600">Gestion Scolaire</p>
      </div>

      <nav className="p-4">
        <ul className="space-y-2">
          {filteredMenuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            const hasChildren = item.children && item.children.length > 0;
            const isSubmenuOpen = openSubmenus[item.path];

            return (
              <li key={item.path}>
                {hasChildren ? (
                  <>
                    <button
                      onClick={() => toggleSubmenu(item.path)}
                      className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <Icon size={20} />
                        <span>{item.name}</span>
                      </div>
                      <ChevronIcon isOpen={isSubmenuOpen} />
                    </button>
                    {isSubmenuOpen && (
                      <ul className="ml-8 mt-1 space-y-1">
                        {item.children.map((child) => (
                          <li key={child.path}>
                            <Link
                              to={child.path}
                              className={`block p-2 rounded-lg transition-colors ${
                                location.pathname === child.path
                                  ? 'bg-blue-100 text-blue-700'
                                  : 'text-gray-600 hover:bg-gray-100'
                              }`}
                            >
                              {child.name}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    )}
                  </>
                ) : (
                  <Link
                    to={item.path}
                    className={`flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <Icon size={20} />
                    <span>{item.name}</span>
                  </Link>
                )}
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="absolute bottom-0 w-full p-4 border-t">
        <button
          onClick={handleLogout}
          className="flex items-center space-x-3 p-3 text-gray-700 hover:bg-gray-100 rounded-lg w-full transition-colors"
        >
          <LogOut size={20} />
          <span>Déconnexion</span>
        </button>
      </div>
    </div>
  );
};

const ChevronIcon = ({ isOpen }) => (
  <svg
    className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
  </svg>
);

export default Sidebar;