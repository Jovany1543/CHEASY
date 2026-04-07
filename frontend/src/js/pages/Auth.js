import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useStore } from "../flux/appContext";

// ── tiny helpers ──────────────────────────────────────────────────────────────
const Badge = ({ role }) => (
  <span
    className={`badge rounded-pill px-3 py-2 ${
      role === "teacher" ? "bg-primary" : "bg-success"
    }`}
    style={{ fontSize: "0.7rem", letterSpacing: "0.1em", textTransform: "uppercase" }}
  >
    {role}
  </span>
);

const Alert = ({ msg, type }) =>
  msg ? (
    <div className={`alert alert-${type} alert-dismissible py-2 mt-3`} role="alert">
      <small>{msg}</small>
    </div>
  ) : null;

// ── LOGIN PAGE ────────────────────────────────────────────────────────────────
function LoginPage({ onSwitch }) {
  const { actions } = useStore();
  const navigate = useNavigate();
  const [role, setRole] = useState("teacher");
  const [form, setForm] = useState({ username: "", password: "" });
  const [status, setStatus] = useState({ msg: "", type: "" });
  const [loading, setLoading] = useState(false);

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus({ msg: "", type: "" });
    try {
      const result = await actions.login(role, form);
      if (result.ok) {
        setStatus({ msg: `✓ Logged in as ${role}. Token saved.`, type: "success" });
        setForm({ username: "", password: "" });
        navigate("/dashboard");
      } else {
        setStatus({ msg: result.message, type: "danger" });
      }
    } catch {
      setStatus({ msg: "Could not reach the server.", type: "danger" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" style={{ background: "#0f1117" }}>
      <div className="w-100" style={{ maxWidth: 420, padding: "0 1rem" }}>

        {/* card */}
        <div
          className="rounded-4 p-4 p-md-5"
          style={{ background: "#1a1d27", border: "1px solid #2a2d3a" }}
        >
          {/* header */}
          <div className="mb-4 text-center">
            <div
              className="mx-auto mb-3 d-flex align-items-center justify-content-center rounded-3"
              style={{ width: 52, height: 52, background: "#2a2d3a" }}
            >
              <svg width="26" height="26" fill="none" viewBox="0 0 24 24">
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" fill="#6b7280"/>
              </svg>
            </div>
            <h4 className="fw-bold text-white mb-1">Sign in</h4>
            <p className="text-secondary" style={{ fontSize: "0.85rem" }}>
              Access your classroom portal
            </p>
          </div>

          {/* role toggle */}
          <div
            className="d-flex rounded-3 p-1 mb-4"
            style={{ background: "#0f1117" }}
          >
            {["teacher", "student"].map((r) => (
              <button
                key={r}
                onClick={() => setRole(r)}
                className={`flex-fill border-0 rounded-2 py-2 fw-semibold transition ${
                  role === r ? "text-white" : "text-secondary bg-transparent"
                }`}
                style={{
                  background: role === r ? (r === "teacher" ? "#2563eb" : "#16a34a") : "transparent",
                  fontSize: "0.85rem",
                  transition: "all .2s",
                  cursor: "pointer",
                }}
              >
                {r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>

          {/* form */}
          <form onSubmit={submit}>
            <div className="mb-3">
              <label className="form-label text-secondary" style={{ fontSize: "0.8rem" }}>
                Username
              </label>
              <input
                name="username"
                value={form.username}
                onChange={handle}
                required
                placeholder="Enter username"
                className="form-control border-0 text-white"
                style={{ background: "#0f1117", color: "#fff" }}
              />
            </div>
            <div className="mb-4">
              <label className="form-label text-secondary" style={{ fontSize: "0.8rem" }}>
                Password
              </label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handle}
                required
                placeholder="••••••••"
                className="form-control border-0 text-white"
                style={{ background: "#0f1117" }}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="btn w-100 fw-semibold text-white"
              style={{
                background: role === "teacher" ? "#2563eb" : "#16a34a",
                border: "none",
                padding: "0.65rem",
                borderRadius: 8,
              }}
            >
              {loading ? (
                <span className="spinner-border spinner-border-sm me-2" />
              ) : null}
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>

          <Alert msg={status.msg} type={status.type} />

          <p className="text-center text-secondary mt-4 mb-0" style={{ fontSize: "0.82rem" }}>
            Need to register?{" "}
            <button
              className="btn btn-link p-0 text-primary text-decoration-none"
              style={{ fontSize: "0.82rem" }}
              onClick={onSwitch}
            >
              Create an account
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

// ── REGISTER PAGE ─────────────────────────────────────────────────────────────
function RegisterPage({ onSwitch }) {
  const { actions } = useStore();
  const [role, setRole] = useState("teacher");
  const [form, setForm] = useState({ username: "", password: "", confirm: "" });
  const [status, setStatus] = useState({ msg: "", type: "" });
  const [loading, setLoading] = useState(false);

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirm) {
      setStatus({ msg: "Passwords do not match.", type: "danger" });
      return;
    }
    setLoading(true);
    setStatus({ msg: "", type: "" });
    try {
      const result = await actions.register(role, {
        username: form.username,
        password: form.password,
      });
      if (result.ok) {
        setStatus({ msg: `✓ ${role.charAt(0).toUpperCase() + role.slice(1)} "${result.data.username}" created successfully!`, type: "success" });
        setForm({ username: "", password: "", confirm: "" });
      } else {
        setStatus({ msg: result.message, type: "danger" });
      }
    } catch {
      setStatus({ msg: "Could not reach the server.", type: "danger" });
    } finally {
      setLoading(false);
    }
  };

  const accent = role === "teacher" ? "#2563eb" : "#16a34a";

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" style={{ background: "#0f1117" }}>
      <div className="w-100" style={{ maxWidth: 420, padding: "0 1rem" }}>
        <div
          className="rounded-4 p-4 p-md-5"
          style={{ background: "#1a1d27", border: "1px solid #2a2d3a" }}
        >
          {/* header */}
          <div className="mb-4 text-center">
            <div
              className="mx-auto mb-3 d-flex align-items-center justify-content-center rounded-3"
              style={{ width: 52, height: 52, background: "#2a2d3a" }}
            >
              <svg width="26" height="26" fill="none" viewBox="0 0 24 24">
                <path d="M15 12c2.7 0 4.8-2.1 4.8-4.8S17.7 2.4 15 2.4s-4.8 2.1-4.8 4.8S12.3 12 15 12zm-9 2.4v1.2H3.6v-1.2C3.6 12.8 6 11.6 7.8 11l.3.3C6.9 12.2 6 13.2 6 14.4zm9 0c-3.2 0-9.6 1.6-9.6 4.8v2.4H24.6v-2.4c0-3.2-6.4-4.8-9.6-4.8zM8.4 10.8C7.2 9.9 6 8.7 6 7.2 6 5.1 7.5 3.6 9.6 3.6c.6 0 1.2.15 1.65.45A6.97 6.97 0 0 0 8.4 7.2c0 1.29.39 2.49 1.05 3.51A4.1 4.1 0 0 1 8.4 10.8z" fill="#6b7280"/>
              </svg>
            </div>
            <h4 className="fw-bold text-white mb-1">Create account</h4>
            <p className="text-secondary" style={{ fontSize: "0.85rem" }}>
              Register a new teacher or student
            </p>
          </div>

          {/* role toggle */}
          <div className="d-flex rounded-3 p-1 mb-4" style={{ background: "#0f1117" }}>
            {["teacher", "student"].map((r) => (
              <button
                key={r}
                onClick={() => { setRole(r); setStatus({ msg: "", type: "" }); }}
                className="flex-fill border-0 rounded-2 py-2 fw-semibold"
                style={{
                  background: role === r ? (r === "teacher" ? "#2563eb" : "#16a34a") : "transparent",
                  color: role === r ? "#fff" : "#6b7280",
                  fontSize: "0.85rem",
                  transition: "all .2s",
                  cursor: "pointer",
                }}
              >
                {r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>

          {/* role pill */}
          <div className="mb-3 d-flex align-items-center gap-2">
            <span className="text-secondary" style={{ fontSize: "0.8rem" }}>Registering as:</span>
            <Badge role={role} />
          </div>

          {/* form */}
          <form onSubmit={submit}>
            <div className="mb-3">
              <label className="form-label text-secondary" style={{ fontSize: "0.8rem" }}>
                Username
              </label>
              <input
                name="username"
                value={form.username}
                onChange={handle}
                required
                minLength={3}
                placeholder="Choose a username"
                className="form-control border-0 text-white"
                style={{ background: "#0f1117" }}
              />
            </div>
            <div className="mb-3">
              <label className="form-label text-secondary" style={{ fontSize: "0.8rem" }}>
                Password
              </label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handle}
                required
                minLength={6}
                placeholder="Min. 6 characters"
                className="form-control border-0 text-white"
                style={{ background: "#0f1117" }}
              />
            </div>
            <div className="mb-4">
              <label className="form-label text-secondary" style={{ fontSize: "0.8rem" }}>
                Confirm password
              </label>
              <input
                type="password"
                name="confirm"
                value={form.confirm}
                onChange={handle}
                required
                placeholder="Repeat password"
                className={`form-control border-0 text-white ${
                  form.confirm && form.confirm !== form.password ? "is-invalid" : ""
                }`}
                style={{ background: "#0f1117" }}
              />
              {form.confirm && form.confirm !== form.password && (
                <div className="invalid-feedback">Passwords don't match.</div>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn w-100 fw-semibold text-white"
              style={{ background: accent, border: "none", padding: "0.65rem", borderRadius: 8 }}
            >
              {loading ? <span className="spinner-border spinner-border-sm me-2" /> : null}
              {loading ? "Creating…" : `Create ${role} account`}
            </button>
          </form>

          <Alert msg={status.msg} type={status.type} />

          <p className="text-center text-secondary mt-4 mb-0" style={{ fontSize: "0.82rem" }}>
            Already have an account?{" "}
            <button
              className="btn btn-link p-0 text-primary text-decoration-none"
              style={{ fontSize: "0.82rem" }}
              onClick={onSwitch}
            >
              Sign in
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

// ── ROOT ──────────────────────────────────────────────────────────────────────
export default function Auth() {
  const [page, setPage] = useState("login");

  return (
    <>
      <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css"
      />
      <style>{`
        * { box-sizing: border-box; }
        body { margin: 0; font-family: 'Segoe UI', sans-serif; }
        .form-control:focus {
          box-shadow: 0 0 0 2px rgba(99,102,241,.35);
          background: #0f1117 !important;
          color: #fff !important;
          border-color: transparent !important;
        }
        .form-control::placeholder { color: #4b5563; }
        .form-control { color: #e5e7eb !important; }
      `}</style>

      {page === "login" ? (
        <LoginPage onSwitch={() => setPage("register")} />
      ) : (
        <RegisterPage onSwitch={() => setPage("login")} />
      )}
    </>
  );
}
