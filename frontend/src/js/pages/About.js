import React from 'react';

function About() {
  return (
    <section className="py-5 bg-light">
      <div className="container">

        {/* HEADER */}
        <div className="mb-5 text-center">
          <h1 className="fw-bold">About Cheasy</h1>
          <p className="lead text-muted">
            Making culinary education simple, approachable, and fun for the next generation.
          </p>
        </div>

        {/* INTRO */}
        <div className="row mb-5">
          <div className="col-lg-10 mx-auto text-center">
            <p className="fs-5">
              Cheasy is a culinary learning platform built specifically for high school students.
              Our mission is simple: make cooking easy to learn, exciting to explore, and accessible to everyone.
            </p>
            <p className="text-muted">
              Whether you're stepping into the kitchen for the first time or sharpening your skills,
              Cheasy breaks everything down into clear, step-by-step lessons designed for real learning.
            </p>
          </div>
        </div>

        {/* STORY SECTIONS */}
        <div className="row g-4 align-items-center mb-5">
          <div className="col-lg-5">
            <div className="card shadow-sm border-0 overflow-hidden">
              <img
                src="/ChefIsraelSantiago.jpg"
                alt="Chef Israel Santiago"
                className="img-fluid"
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            </div>
          </div>

          <div className="col-lg-7">
            <h3 className="fw-bold">Meet Chef Izzy</h3>
            <p>
              Chef Israel Santiago, known as Chef Izzy, created Cheasy with one goal in mind:
              to inspire and empower students to feel confident in the kitchen.
            </p>
            <p>
              With real-world culinary experience and a passion for teaching, he believes that
              anyone can become a great cook with the right guidance, structure, and encouragement.
            </p>

            <a
              href="https://www.linkedin.com/in/isantiago12/"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline-dark mt-2"
            >
              View LinkedIn
            </a>
          </div>
        </div>

        <div className="row g-4 align-items-center mb-5">
          <div className="col-lg-7 order-2 order-lg-1">
            <h3 className="fw-bold">Hands-On Culinary Training</h3>
            <p>
              Cheasy is built around practice, not just theory. Students learn by working through
              real kitchen skills, guided exercises, and repeatable routines that make cooking feel natural.
            </p>
            <p className="text-muted mb-0">
              The goal is to turn curiosity into confidence by showing students exactly what to do,
              why it matters, and how to improve with each lesson.
            </p>
          </div>

          <div className="col-lg-5 order-1 order-lg-2">
            <div className="card shadow-sm border-0 overflow-hidden h-100">
              <img
                src="/culinarytraining2017.jpg"
                alt="Students participating in culinary training"
                className="img-fluid"
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            </div>
          </div>
        </div>

        <div className="row g-4 align-items-center mb-5">
          <div className="col-lg-5">
            <div className="card shadow-sm border-0 overflow-hidden h-100">
              <img
                src="/StockCake-Cooking_Class_Focus-1237074-medium.jpg"
                alt="Hands-on cooking class session"
                className="img-fluid"
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            </div>
          </div>

          <div className="col-lg-7">
            <h3 className="fw-bold">Focused Learning in Every Lesson</h3>
            <p>
              Every Cheasy lesson is designed to keep students engaged without overwhelming them.
              Instead of throwing too much information at once, the platform breaks techniques into
              simple, achievable steps.
            </p>
            <p className="text-muted mb-0">
              That structure helps learners stay motivated, track their progress, and build real
              kitchen habits they can carry beyond the classroom.
            </p>
          </div>
        </div>

        {/* GOAL SECTION */}
        <div className="text-center">
          <h3 className="fw-bold">Our Goal</h3>
          <p className="mx-auto" style={{ maxWidth: '700px' }}>
            We aim to give students confidence in the kitchen and show that learning to cook
            doesn’t have to be complicated. With the right approach, the right tools, and the
            right mindset—it can be Cheasy.
          </p>

          <button className="btn btn-warning btn-lg mt-3">
            Start Learning
          </button>
        </div>

      </div>
    </section>
  );
}

export default About;