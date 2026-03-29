// ============================================================
// VRMS - Vehicle Rental Management System
// Frontend: React + Tailwind CSS
// AI Disclosure: Portions generated/assisted by Claude (Anthropic).
//   Developer remains fully responsible for final code.
// ============================================================

import { useState, useEffect } from "react";

const API = "http://localhost:8000";

// ── Shared helpers ─────────────────────────────────────────────
const StatusBadge = ({ status }) => {
  const colors = {
    Booked:    "bg-blue-100 text-blue-700",
    Active:    "bg-green-100 text-green-700",
    Completed: "bg-gray-100 text-gray-600",
    Cancelled: "bg-red-100 text-red-600",
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${colors[status] ?? "bg-yellow-100 text-yellow-700"}`}>
      {status}
    </span>
  );
};

const fmt = (val) => (val ? new Date(val).toLocaleString() : "—");
const money = (val) => (val != null ? `$${parseFloat(val).toFixed(2)}` : "—");

// ── NAV ────────────────────────────────────────────────────────
const NAV_ITEMS = [
  { id: "vehicles",    label: "🚗 Vehicles" },
  { id: "add-vehicle", label: "➕ Add Vehicle" },
  { id: "agreements",  label: "📋 Rental Agreements" },
  { id: "customers",   label: "👤 Customers" },
];

// ══════════════════════════════════════════════════════════════
// PAGE: Vehicle List
// ══════════════════════════════════════════════════════════════
function VehiclesPage() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/vehicles`)
      .then((r) => r.json())
      .then((d) => { setVehicles(d); setLoading(false); })
      .catch(() => { setError("Failed to load vehicles."); setLoading(false); });
  }, []);

  if (loading) return <Spinner />;
  if (error)   return <ErrorBox msg={error} />;

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Fleet Overview</h2>
      <div className="overflow-x-auto rounded-xl border border-gray-200 shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-indigo-600 text-white">
            <tr>
              {["ID","Plate","Make","Model","Year","Color","Type","Rate/Day","Mileage","Branch"].map(h => (
                <th key={h} className="px-4 py-3 text-left font-semibold whitespace-nowrap">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {vehicles.length === 0 ? (
              <tr><td colSpan={10} className="text-center py-8 text-gray-400">No vehicles found.</td></tr>
            ) : vehicles.map((v, i) => (
              <tr key={v.VehicleID} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                <td className="px-4 py-2 text-gray-500">{v.VehicleID}</td>
                <td className="px-4 py-2 font-mono font-medium text-indigo-700">{v.LicensePlate}</td>
                <td className="px-4 py-2">{v.Make}</td>
                <td className="px-4 py-2">{v.Model}</td>
                <td className="px-4 py-2">{v.Year}</td>
                <td className="px-4 py-2">{v.Color ?? "—"}</td>
                <td className="px-4 py-2">
                  <span className="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full text-xs font-medium">
                    {v.TypeName}
                  </span>
                </td>
                <td className="px-4 py-2 font-medium text-green-700">${parseFloat(v.DailyRentalRate).toFixed(2)}</td>
                <td className="px-4 py-2 text-gray-500">{v.CurrentMileage.toLocaleString()} mi</td>
                <td className="px-4 py-2 text-gray-600">{v.BranchName}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
// PAGE: Add Vehicle
// ══════════════════════════════════════════════════════════════
function AddVehiclePage() {
  const [types,    setTypes]    = useState([]);
  const [branches, setBranches] = useState([]);
  const [form, setForm] = useState({
    LicensePlate: "", Make: "", Model: "", Year: new Date().getFullYear(),
    Color: "", DailyRentalRate: "", CurrentMileage: "0", TypeID: "", BranchID: "",
  });
  const [errors,  setErrors]  = useState({});
  const [success, setSuccess] = useState("");
  const [apiErr,  setApiErr]  = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/vehicle-types`).then(r => r.json()).then(setTypes);
    fetch(`${API}/branches`).then(r => r.json()).then(setBranches);
  }, []);

  const validate = () => {
    const e = {};
    if (!form.LicensePlate.trim()) e.LicensePlate = "License plate is required.";
    if (!form.Make.trim())         e.Make = "Make is required.";
    if (!form.Model.trim())        e.Model = "Model is required.";
    const yr = parseInt(form.Year);
    if (isNaN(yr) || yr < 1900 || yr > new Date().getFullYear() + 1)
      e.Year = `Year must be between 1900 and ${new Date().getFullYear() + 1}.`;
    const rate = parseFloat(form.DailyRentalRate);
    if (isNaN(rate) || rate <= 0) e.DailyRentalRate = "Daily rate must be a positive number.";
    const mi = parseInt(form.CurrentMileage);
    if (isNaN(mi) || mi < 0)      e.CurrentMileage = "Mileage must be 0 or greater.";
    if (!form.TypeID)              e.TypeID = "Please select a vehicle type.";
    if (!form.BranchID)            e.BranchID = "Please select a branch.";
    return e;
  };

  const handleChange = (e) => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
    setErrors(ev => ({ ...ev, [e.target.name]: undefined }));
    setSuccess(""); setApiErr("");
  };

  const handleSubmit = async () => {
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    setLoading(true); setApiErr(""); setSuccess("");
    try {
      const res = await fetch(`${API}/vehicles`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          Year: parseInt(form.Year),
          DailyRentalRate: parseFloat(form.DailyRentalRate),
          CurrentMileage: parseInt(form.CurrentMileage),
          TypeID: parseInt(form.TypeID),
          BranchID: parseInt(form.BranchID),
          LicensePlate: form.LicensePlate.trim().toUpperCase(),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail ?? "Failed to add vehicle.");
      setSuccess(`✅ Vehicle added successfully! (ID: ${data.VehicleID})`);
      setForm({ LicensePlate: "", Make: "", Model: "", Year: new Date().getFullYear(),
                Color: "", DailyRentalRate: "", CurrentMileage: "0", TypeID: "", BranchID: "" });
    } catch (err) {
      setApiErr(err.message);
    } finally {
      setLoading(false);
    }
  };

  const Field = ({ label, name, type = "text", placeholder, required }) => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        type={type}
        name={name}
        value={form[name]}
        onChange={handleChange}
        placeholder={placeholder}
        className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400
          ${errors[name] ? "border-red-400 bg-red-50" : "border-gray-300"}`}
      />
      {errors[name] && <p className="text-xs text-red-500 mt-1">{errors[name]}</p>}
    </div>
  );

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold text-gray-800 mb-1">Add New Vehicle</h2>
      <p className="text-sm text-gray-500 mb-6">Fill in all required fields to register a vehicle in the fleet.</p>

      {success && <div className="mb-4 p-3 bg-green-50 border border-green-300 text-green-700 rounded-lg text-sm">{success}</div>}
      {apiErr  && <div className="mb-4 p-3 bg-red-50 border border-red-300 text-red-700 rounded-lg text-sm">❌ {apiErr}</div>}

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Field label="License Plate" name="LicensePlate" placeholder="FL-AAA-000" required />
          <Field label="Year" name="Year" type="number" placeholder="2024" required />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Make" name="Make" placeholder="Toyota" required />
          <Field label="Model" name="Model" placeholder="Camry" required />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Color" name="Color" placeholder="Silver" />
          <Field label="Daily Rental Rate ($)" name="DailyRentalRate" type="number" placeholder="55.00" required />
        </div>
        <Field label="Current Mileage (mi)" name="CurrentMileage" type="number" placeholder="0" required />

        {/* Vehicle Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Vehicle Type <span className="text-red-500">*</span>
          </label>
          <select
            name="TypeID" value={form.TypeID} onChange={handleChange}
            className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400
              ${errors.TypeID ? "border-red-400 bg-red-50" : "border-gray-300"}`}
          >
            <option value="">— Select type —</option>
            {types.map(t => <option key={t.TypeID} value={t.TypeID}>{t.TypeName}</option>)}
          </select>
          {errors.TypeID && <p className="text-xs text-red-500 mt-1">{errors.TypeID}</p>}
        </div>

        {/* Branch */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Branch <span className="text-red-500">*</span>
          </label>
          <select
            name="BranchID" value={form.BranchID} onChange={handleChange}
            className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400
              ${errors.BranchID ? "border-red-400 bg-red-50" : "border-gray-300"}`}
          >
            <option value="">— Select branch —</option>
            {branches.map(b => <option key={b.BranchID} value={b.BranchID}>{b.Name} — {b.Address}</option>)}
          </select>
          {errors.BranchID && <p className="text-xs text-red-500 mt-1">{errors.BranchID}</p>}
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold py-2.5 rounded-lg transition-colors"
        >
          {loading ? "Saving…" : "Add Vehicle"}
        </button>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
// PAGE: Rental Agreements
// ══════════════════════════════════════════════════════════════
function AgreementsPage() {
  const [customerID, setCustomerID] = useState("");
  const [input,      setInput]      = useState("");
  const [data,       setData]       = useState(null);
  const [loading,    setLoading]    = useState(false);
  const [error,      setError]      = useState("");

  const search = async () => {
    const id = parseInt(input.trim());
    if (isNaN(id) || id <= 0) { setError("Please enter a valid positive Customer ID."); return; }
    setLoading(true); setError(""); setData(null);
    try {
      const res = await fetch(`${API}/rental-agreements?customer_id=${id}`);
      const json = await res.json();
      if (!res.ok) throw new Error(json.detail ?? "Error fetching agreements.");
      setData(json); setCustomerID(id);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-1">Rental Agreements</h2>
      <p className="text-sm text-gray-500 mb-6">Look up all rental agreements for a specific customer.</p>

      {/* Search bar */}
      <div className="flex gap-3 mb-6 max-w-md">
        <input
          type="number"
          value={input}
          onChange={e => { setInput(e.target.value); setError(""); }}
          onKeyDown={e => e.key === "Enter" && search()}
          placeholder="Enter Customer ID…"
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          onClick={search}
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg text-sm font-semibold disabled:opacity-50"
        >
          {loading ? "…" : "Search"}
        </button>
      </div>

      {error && <ErrorBox msg={error} />}

      {data && (
        <>
          {/* Customer card */}
          <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-4 mb-5 flex items-center gap-3">
            <div className="bg-indigo-600 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold text-sm">
              {data.customer.FirstName[0]}{data.customer.LastName[0]}
            </div>
            <div>
              <p className="font-semibold text-gray-800">{data.customer.FirstName} {data.customer.LastName}</p>
              <p className="text-xs text-gray-500">Customer ID: {data.customer.CustomerID}</p>
            </div>
            <span className="ml-auto bg-indigo-100 text-indigo-700 text-xs font-semibold px-3 py-1 rounded-full">
              {data.agreements.length} agreement{data.agreements.length !== 1 ? "s" : ""}
            </span>
          </div>

          {data.agreements.length === 0 ? (
            <p className="text-gray-400 text-sm">No rental agreements found for this customer.</p>
          ) : (
            <div className="space-y-4">
              {data.agreements.map(a => (
                <div key={a.AgreementID} className="bg-white border border-gray-200 rounded-xl shadow-sm p-5">
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-gray-700">Agreement #{a.AgreementID}</span>
                    <StatusBadge status={a.Status} />
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-6 gap-y-2 text-sm">
                    <Info label="Vehicle"   value={`${a.Year} ${a.Make} ${a.Model}`} />
                    <Info label="Plate"     value={a.LicensePlate} mono />
                    <Info label="Type"      value={a.TypeName} />
                    <Info label="Pickup From" value={a.PickupBranch} />
                    <Info label="Return To"   value={a.ReturnBranch} />
                    <Info label="Est. Cost"   value={money(a.EstimatedCost)} />
                    <Info label="Sched. Pickup" value={fmt(a.ScheduledPickupDateTime)} />
                    <Info label="Sched. Return" value={fmt(a.ScheduledReturnDateTime)} />
                    <Info label="Actual Cost"   value={money(a.ActualCost)} />
                    {a.ActualPickupDateTime && <Info label="Actual Pickup" value={fmt(a.ActualPickupDateTime)} />}
                    {a.ActualReturnDateTime && <Info label="Actual Return" value={fmt(a.ActualReturnDateTime)} />}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

const Info = ({ label, value, mono }) => (
  <div>
    <p className="text-xs text-gray-400 uppercase tracking-wide">{label}</p>
    <p className={`text-gray-700 font-medium ${mono ? "font-mono text-indigo-700" : ""}`}>{value}</p>
  </div>
);

// ══════════════════════════════════════════════════════════════
// PAGE: Customers
// ══════════════════════════════════════════════════════════════
function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [loading,   setLoading]   = useState(true);
  const [error,     setError]     = useState("");

  useEffect(() => {
    fetch(`${API}/customers`)
      .then(r => r.json())
      .then(d => { setCustomers(d); setLoading(false); })
      .catch(() => { setError("Failed to load customers."); setLoading(false); });
  }, []);

  if (loading) return <Spinner />;
  if (error)   return <ErrorBox msg={error} />;

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Customers</h2>
      <div className="overflow-x-auto rounded-xl border border-gray-200 shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-indigo-600 text-white">
            <tr>
              {["ID","First Name","Last Name","Phone","Email","License #","License Expiry"].map(h => (
                <th key={h} className="px-4 py-3 text-left font-semibold whitespace-nowrap">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {customers.length === 0 ? (
              <tr><td colSpan={7} className="text-center py-8 text-gray-400">No customers found.</td></tr>
            ) : customers.map((c, i) => (
              <tr key={c.CustomerID} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                <td className="px-4 py-2 text-gray-400">{c.CustomerID}</td>
                <td className="px-4 py-2 font-medium">{c.FirstName}</td>
                <td className="px-4 py-2 font-medium">{c.LastName}</td>
                <td className="px-4 py-2 text-gray-600">{c.PhoneNumber}</td>
                <td className="px-4 py-2 text-indigo-700">{c.Email}</td>
                <td className="px-4 py-2 font-mono text-xs">{c.DriversLicenseNumber}</td>
                <td className="px-4 py-2">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                    new Date(c.DriversLicenseExpiryDate) > new Date()
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-600"
                  }`}>
                    {c.DriversLicenseExpiryDate}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ── Utility components ─────────────────────────────────────────
const Spinner = () => (
  <div className="flex items-center justify-center py-16 text-indigo-500">
    <svg className="animate-spin h-8 w-8" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
    </svg>
  </div>
);

const ErrorBox = ({ msg }) => (
  <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">❌ {msg}</div>
);

// ══════════════════════════════════════════════════════════════
// ROOT APP
// ══════════════════════════════════════════════════════════════
export default function App() {
  const [page, setPage] = useState("vehicles");

  const pages = {
    vehicles:    <VehiclesPage />,
    "add-vehicle": <AddVehiclePage />,
    agreements:  <AgreementsPage />,
    customers:   <CustomersPage />,
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-indigo-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
          <span className="text-2xl">🚘</span>
          <div>
            <h1 className="text-xl font-bold leading-tight">DriveEasy Rentals</h1>
            <p className="text-indigo-300 text-xs">Vehicle Rental Management System</p>
          </div>
        </div>
      </header>

      {/* Nav */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 flex gap-1">
          {NAV_ITEMS.map(n => (
            <button
              key={n.id}
              onClick={() => setPage(n.id)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                page === n.id
                  ? "border-indigo-600 text-indigo-700"
                  : "border-transparent text-gray-500 hover:text-gray-800 hover:border-gray-300"
              }`}
            >
              {n.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        {pages[page]}
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-4 border-t border-gray-100">
        VRMS © 2025 — DriveEasy Rentals
      </footer>
    </div>
  );
}