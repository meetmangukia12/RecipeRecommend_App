import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const location = useLocation();
  const isHome = location.pathname === "/";

  if (isHome) return null;

  return (
    <div className="navbar">
      {/* Clickable logo that links to home */}
      <Link to="/" className="navbar-logo">
        Recipe<span style={{ color: "#3b82f6" }}>Hub</span>
      </Link>

    </div>
  );
};

export default Navbar;
