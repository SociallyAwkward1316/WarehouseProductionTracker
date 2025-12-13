# Warehouse Production Tracker

## Overview

The Warehouse Production Tracker is a production-ready Django web application built to help warehouse associates track, visualize, and improve their daily production performance.

This project was inspired by a real workplace need. Several of my coworkers asked if I could build something simple to help them track their daily moves and production percentages, since everything was previously purely shown as a total of moves toward the end of the workshift. This app was built to solve that problem in a clean, reliable, and accessible way.

It is fully deployed with PostgreSQL in production and uses Django’s templating engine to deliver a fast, server-rendered experience.

## Key Features

- User authentication (registration & login)
- Shift-based production tracking per user
- Automatic production percentage calculation
- Interactive production-over-time chart
- Clean server-rendered UI using Django templates
- Secure session and CSRF configuration for production
- PostgreSQL-backed production database

## Tech Stack

- **Backend:** Django 5
- **Database:** PostgreSQL (hosted on Render)
- **Frontend:** Django Templates (server-rendered)
- **Charting:** Plotly
- **Deployment:** Render
- **Environment Management:** django-environ

## Architecture Notes

- Each user has isolated production data
- Shifts are stored relationally and queried per-user
- Charts are dynamically generated from live database data
- Production settings are handled via environment variables
- Static files are collected at deploy time for production use

## Authentication

This application uses Django’s built-in authentication system with standard session-based login and logout flows.

The app is fully server-rendered using Django templates and relies on Django’s default session handling for authentication. There is no frontend framework, no JWT-based authentication, no localStorage usage, and no custom cookie logic implemented.


## Deployment

The application is deployed as a Render Web Service with a managed PostgreSQL database.

Production setup includes:

- `DEBUG=False`
- CSRF trusted origins configured
- Database connection via `DATABASE_URL`

## Why This Project Matters

This project represents a real-world solution to a real problem, not a tutorial or sample app.

It demonstrates:

- End-to-end Django development
- Production database setup and migrations
- Deployment debugging and issue resolution
- Building tools based on user feedback and real requirements

## Future Improvements

- Exportable production reports
- Mobile-first UI enhancements

## Author

Built by me(Alexis Fuenmayor) a backend-focused developer with hands-on experience deploying and maintaining real production Django applications.
