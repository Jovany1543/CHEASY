import React from 'react';

function Home() {
  return (
    <div>
      {/* HERO SECTION */}
      <section
        className="d-flex align-items-center"
        style={{
          minHeight: '80vh',
          padding: '48px 32px',
          color: '#fff',
          backgroundImage:
            "linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), url('/978a4804-e40d-4450-8bf0-d16462e53575.png')",
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          backgroundSize: 'cover',
        }}
      >
        <div className="container text-start">
          <h1 className="display-4 fw-bold">Learn to Cook the Cheasy Way</h1>
          <p className="lead mt-3">
            Real skills. Real recipes. No stress. Start your culinary journey today.
          </p>
          <div className="mt-4">
            <button className="btn btn-warning btn-lg me-3">Start Learning</button>
            <button className="btn btn-outline-light btn-lg">Explore Recipes</button>
          </div>
        </div>
      </section>

      {/* ABOUT PREVIEW */}
      <section className="py-5 bg-light text-dark">
        <div className="container">
          <h2 className="mb-3">Cooking Made Simple</h2>
          <p>
            Cheasy is built for students who want to learn how to cook without feeling overwhelmed.
            Whether you're just starting or improving your skills, we make everything easy to follow.
          </p>
        </div>
      </section>

      {/* FEATURES */}
      <section className="py-5 text-center">
        <div className="container">
          <h2 className="mb-5">Why Cheasy?</h2>
          <div className="row">
            <div className="col-md-4 mb-4">
              <h5>Step-by-Step Lessons</h5>
              <p>Clear instructions that guide you through every recipe.</p>
            </div>
            <div className="col-md-4 mb-4">
              <h5>Beginner-Friendly</h5>
              <p>Start simple and build confidence in the kitchen.</p>
            </div>
            <div className="col-md-4 mb-4">
              <h5>Chef Guidance</h5>
              <p>Learn real techniques from a professional chef.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-5 bg-dark text-white text-center">
        <div className="container">
          <h2>Ready to Start Cooking?</h2>
          <p className="mt-3">
            Your first recipe is just a click away.
          </p>
          <button className="btn btn-warning btn-lg mt-3">
            Get Started
          </button>
        </div>
      </section>
    </div>
  );
}

export default Home;