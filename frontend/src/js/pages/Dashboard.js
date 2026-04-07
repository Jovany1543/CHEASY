import React from 'react';

export function TeacherDashboard() {
  // 🔥 Mock data (replace with API later)
  const courses = [
    {
      id: 1,
      title: "Intro to Cooking",
      students: [
        { id: 1, name: "John Doe", email: "john@email.com" },
        { id: 2, name: "Jane Smith", email: "jane@email.com" }
      ]
    },
    {
      id: 2,
      title: "Baking Basics",
      students: [
        { id: 3, name: "Mike Ross", email: "mike@email.com" }
      ]
    }
  ];

  return (
    <div className="container py-5">
      <h1 className="mb-4">👨‍🍳 Teacher Dashboard</h1>

      {/* SUMMARY CARDS */}
      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card p-3 shadow-sm">
            <h5>Total Courses</h5>
            <h3>{courses.length}</h3>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card p-3 shadow-sm">
            <h5>Total Students</h5>
            <h3>
              {courses.reduce((acc, c) => acc + c.students.length, 0)}
            </h3>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card p-3 shadow-sm">
            <h5>Active Classes</h5>
            <h3>{courses.length}</h3>
          </div>
        </div>
      </div>

      {/* COURSES */}
      <h2 className="mb-3">Your Courses</h2>

      {courses.map(course => (
        <div key={course.id} className="card mb-4 shadow-sm">
          <div className="card-body">
            <div className="d-flex justify-content-between align-items-center">
              <h4>{course.title}</h4>
              <button className="btn btn-sm btn-warning">
                Add Student
              </button>
            </div>

            <p className="text-muted">
              {course.students.length} students enrolled
            </p>

            {/* STUDENTS TABLE */}
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {course.students.map(student => (
                    <tr key={student.id}>
                      <td>{student.name}</td>
                      <td>{student.email}</td>
                      <td>
                        <button className="btn btn-sm btn-outline-danger me-2">
                          Remove
                        </button>
                        <button className="btn btn-sm btn-outline-primary">
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

          </div>
        </div>
      ))}

      {/* ACTION BUTTON */}
      <button className="btn btn-dark btn-lg">
        + Create New Course
      </button>
    </div>
  );
}




export function StudentDashboard() {
  // 🔥 Mock data
  const courses = [
    {
      id: 1,
      title: "Intro to Cooking",
      progress: 60
    },
    {
      id: 2,
      title: "Baking Basics",
      progress: 25
    }
  ];

  return (
    <div className="container py-5">
      <h1 className="mb-4">🎓 Student Dashboard</h1>

      {/* SUMMARY */}
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="card p-3 shadow-sm">
            <h5>Enrolled Courses</h5>
            <h3>{courses.length}</h3>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card p-3 shadow-sm">
            <h5>Average Progress</h5>
            <h3>
              {Math.round(
                courses.reduce((acc, c) => acc + c.progress, 0) /
                  courses.length
              )}
              %
            </h3>
          </div>
        </div>
      </div>

      {/* COURSES */}
      <h2 className="mb-3">My Courses</h2>

      <div className="row">
        {courses.map(course => (
          <div key={course.id} className="col-md-6 mb-4">
            <div className="card shadow-sm p-3">
              <h5>{course.title}</h5>

              {/* PROGRESS BAR */}
              <div className="progress my-3">
                <div
                  className="progress-bar bg-warning"
                  role="progressbar"
                  style={{ width: `${course.progress}%` }}
                >
                  {course.progress}%
                </div>
              </div>

              <button className="btn btn-dark">
                Continue Course
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

