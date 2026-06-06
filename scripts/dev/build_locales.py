"""Generate locale JSON files from data.js plus about/contact/ui content."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCALES_DIR = ROOT / "assets" / "locales"


def load_data_js() -> dict:
    raw = (ROOT / "assets" / "js" / "data.js").read_text(encoding="utf-8")
    return json.loads(raw.split("=", 1)[1].rsplit(";", 1)[0].strip())


def build_about_en() -> dict:
    return {
        "pageTitle": "About Powerlink Energy",
        "pageDescription": "Learn how Powerlink Energy approaches integrated power supply for critical applications.",
        "hero": {
            "eyebrow": "About Us",
            "title": "About Powerlink Energy",
            "body": "Powerlink Energy is a solution-driven supplier specializing in integrated power systems for critical applications.",
            "primaryButton": "Explore Solutions",
            "secondaryButton": "Talk to Our Team",
            "image": "/downloads/supplier_images/易事特集团股份有限公司/products/003-optimized.jpg",
            "imageAlt": "Integrated power and energy storage equipment",
            "overlayEyebrow": "Professional Positioning",
            "overlayTitle": "Scenario-first, integration-focused",
            "overlayBody": "Built for customers who need practical project support instead of a generic product list.",
        },
        "why": {
            "eyebrow": "Why Powerlink Energy",
            "title": "Built Around Workable Power Solutions",
            "body": "We focus on how power hosts, batteries, conversion equipment, cabling, and monitoring accessories work together in real projects.",
            "cards": [
                {
                    "index": "01",
                    "title": "Scenario-Based Thinking",
                    "body": "We match products around applications such as data centers, telecom sites, storage projects, and edge environments.",
                },
                {
                    "index": "02",
                    "title": "Integrated Supply",
                    "body": "We combine UPS, battery systems, DC/DC modules, inverters, and accessories into one practical sourcing path.",
                },
                {
                    "index": "03",
                    "title": "Fast Response",
                    "body": "We prioritize clear communication, quick matching, and timely follow-up during quotation and project discussion.",
                },
                {
                    "index": "04",
                    "title": "Flexible Cooperation",
                    "body": "We support both small-batch orders and longer-term project cooperation for customers who need practical supply support.",
                },
            ],
        },
        "whatWeDo": {
            "eyebrow": "What We Do",
            "title": "Integrated Categories for Critical Applications",
            "body1": "We focus on combining practical products into workable power solutions for customers in data centers, telecom infrastructure, energy storage, edge computing, and other power-sensitive environments.",
            "body2": "Instead of only offering standalone products, we emphasize application-based matching and one-stop integration.",
            "categories": [
                "UPS systems",
                "Lithium battery storage",
                "Solar and hybrid inverters",
                "Telecom power systems",
                "DC/DC modules",
                "Industrial M12 cabling",
                "Monitoring and sensing accessories",
            ],
        },
        "whyChooseUs": {
            "eyebrow": "Why Choose Us",
            "title": "Professional and Dependable",
            "body": "We believe good supply support is not only about product availability. It is also about faster response, clearer communication, practical matching, and dependable follow-up.",
            "points": [
                {"label": "Scenario coverage:", "value": "data center, telecom, storage, edge, monitoring"},
                {"label": "Cooperation style:", "value": "flexible for both project and phased purchasing"},
                {"label": "Communication:", "value": "direct, responsive, and solution-oriented"},
            ],
        },
        "howWeWork": {
            "eyebrow": "How We Work",
            "title": "Practical Collaboration Process",
            "body": "We keep the process simple: understand the application, match the configuration, and support communication through quotation and delivery coordination.",
            "steps": [
                {"title": "Understand", "body": "Review the application, power requirement, and market context."},
                {"title": "Match", "body": "Combine the right product categories into a practical solution path."},
                {"title": "Support", "body": "Coordinate quotation, sourcing, and delivery communication clearly."},
            ],
        },
        "cta": {
            "eyebrow": "Next Step",
            "title": "Talk to Us About Your Application",
            "body": "If you are looking for a practical power solution instead of a generic product list, Powerlink Energy is ready to support your project.",
            "primaryButton": "Contact Us",
            "secondaryButton": "Explore Solutions",
        },
    }


def build_contact_en() -> dict:
    return {
        "heroImage": "/downloads/supplier_images/深圳索瑞德电子有限公司/products/010-optimized.jpg",
        "heroImageAlt": "Integrated telecom and backup power equipment for project inquiries",
        "pageTitle": "Contact Us | Powerlink Energy",
        "pageDescription": "Contact Powerlink Energy for UPS, battery, inverter, telecom power, and integrated solution inquiries.",
        "eyebrow": "Contact",
        "title": "Contact Us",
        "heroBody": "Tell us what you need, and we will help you match the right solution for your application.",
        "emailButton": "Email Us",
        "whatsappButton": "WhatsApp Us",
        "overlayEyebrow": "Direct Communication",
        "overlayTitle": "Fast project response",
        "overlayBody": "Share your application, target market, and requirement range. We will help you match the right direction quickly.",
        "directContactEyebrow": "Direct Contact",
        "directContactTitle": "Reach Our Team Directly",
        "directContactBody": "Looking for UPS systems, battery storage, telecom power equipment, industrial cabling, or a customized power solution package? Send us your project details and we will get back to you as soon as possible.",
        "emailLabel": "Email",
        "whatsappLabel": "WhatsApp",
        "websiteLabel": "Website",
        "promiseSteps": [
            {
                "title": "Application first",
                "body": "Tell us the scenario and target market so we can match the right solution path.",
            },
            {
                "title": "Clear communication",
                "body": "We keep the discussion practical around requirement range, product scope, and quantity.",
            },
            {
                "title": "Fast follow-up",
                "body": "We prioritize timely feedback for customers who are evaluating or preparing a project inquiry.",
            },
        ],
        "formEyebrow": "Inquiry Form",
        "formTitle": "Send Your Inquiry",
        "formIntro": "To help us respond faster, please include your application scenario, power range, target market, estimated quantity, and product category of interest.",
        "formNote": "Submitting this form opens your default email client with a prefilled inquiry. If no mail client is available, contact us directly by email or WhatsApp.",
        "formLabels": {
            "name": "Name",
            "company": "Company",
            "country": "Country",
            "email": "Email",
            "whatsapp": "WhatsApp",
            "application": "Application",
            "productInterest": "Product Interest",
            "message": "Message",
        },
        "formSubmit": "Send Your Inquiry",
    }


def build_ui_en() -> dict:
    return {
        "nav": {
            "toggleAria": "Toggle navigation",
            "menu": "Menu",
            "primaryAria": "Primary navigation",
        },
        "footer": {
            "brand": "Powerlink Energy",
            "tagline": "Scenario-first supply support for power-sensitive and mission-critical applications.",
            "directContact": "Direct Contact",
        },
        "noscript": "JavaScript is optional on this site. Core navigation and page content remain available without it.",
        "buttons": {
            "exploreSolutions": "Explore Solutions",
            "getQuote": "Get a Quote",
            "learnMore": "Learn more",
            "exploreSolution": "Explore solution",
            "viewDetails": "View details",
            "backTo": "Back to {label}",
            "emailUs": "Email Us",
            "whatsappUs": "WhatsApp Us",
            "contactUs": "Contact Us",
            "talkToTeam": "Talk to Our Team",
            "sendInquiry": "Send Your Inquiry",
        },
        "labels": {
            "email": "Email:",
            "whatsapp": "WhatsApp:",
            "website": "Website:",
        },
        "cards": {
            "solution": "Solution",
            "product": "Product",
            "verifiedProjectAssets": "Verified Project Assets",
            "projectVisualsLater": "Project visuals will be added later",
            "verifiedMediaFallback": "Verified project media will be added after approval.",
        },
        "metrics": {
            "solutionScenarios": "solution scenarios",
            "productCategories": "product categories",
            "referenceFrameworks": "reference frameworks",
            "integratedSupplyPath": "integrated supply path",
        },
        "home": {
            "eyebrow": "Powerlink Energy",
            "applications": {
                "eyebrow": "Applications We Serve",
                "title": "Practical Support for Mission-Critical Environments",
                "body": "We support customers in power-sensitive and mission-critical environments with practical, scenario-based solutions.",
            },
            "solutions": {
                "eyebrow": "Scenario-Based Solutions",
                "title": "Solutions Built Around Real Applications",
                "body": "Instead of offering only standalone products, we help customers combine the right equipment into workable power solution packages.",
            },
            "products": {
                "eyebrow": "Product Categories",
                "title": "Core Equipment Categories",
                "body": "Our product portfolio supports both standard supply and integrated project configurations.",
            },
            "cases": {
                "eyebrow": "Reference Frameworks",
                "title": "Reference Structures That Can Scale",
                "body": "Our reference frameworks explain typical application structures now and can evolve into a verified project library later.",
            },
            "advantages": {
                "eyebrow": "Why Powerlink Energy",
                "title": "Fast Response, Practical Matching, One Supply Path",
            },
            "contact": {
                "eyebrow": "Talk to Us About Your Application",
                "title": "Send Your Application Brief and We Will Match the Right Direction",
                "body": "Tell us your application, power requirement, and target market. We will help you match the right solution quickly.",
            },
        },
        "pages": {
            "home": {
                "title": "Powerlink Energy | Integrated Power Solutions",
                "description": "Scenario-driven power solutions for data centers, telecom sites, energy storage, and other critical applications.",
            },
            "solutions": {
                "title": "Solutions | Powerlink Energy",
                "description": "Explore scenario-based integrated power solutions from Powerlink Energy.",
                "overviewTitle": "Scenario-Based Power Solutions",
                "overviewDescription": "Instead of offering only standalone products, we help customers combine the right equipment into workable power solution packages.",
            },
            "products": {
                "title": "Products | Powerlink Energy",
                "description": "Explore Powerlink Energy product categories for UPS, batteries, inverters, telecom power, and monitoring accessories.",
                "overviewTitle": "Product Categories for Direct Category Buyers",
                "overviewDescription": "Our product portfolio supports both standard supply and integrated project configurations for buyers who already know their technical category.",
            },
            "cases": {
                "title": "Reference Frameworks | Powerlink Energy",
                "description": "Explore Powerlink Energy reference frameworks for recurring application structures and future project libraries.",
                "overviewTitle": "Reference Frameworks for Future Project Expansion",
                "overviewDescription": "This section presents reusable application structures and reference content that can grow into a verified project library later.",
            },
        },
        "casesHero": {
            "eyebrow": "Reference Frameworks",
            "title": "Reference Frameworks That Can Grow Into a Real Case Library",
            "body": "Use structured framework content to explain applications clearly now and add verified project photos later without changing the page system.",
            "pills": ["Scenario-led", "Expandable", "Project-ready"],
            "panelEyebrow": "How We Structure Frameworks",
            "panelTitle": "Application first, assets second",
            "panelBody": "Each page explains the typical need, design logic, recommended configuration, and future project media in one reusable template.",
        },
        "detail": {
            "ctaEyebrow": "Talk to Powerlink Energy",
            "ctaTitle": "Need practical product matching for your application?",
            "ctaBody": "Tell us your application, target market, and expected quantity. We will help you match the right solution quickly.",
            "solutionEyebrow": "Solution Detail",
            "solutionPills": ["Scenario-driven content", "Integrated support", "Practical delivery path"],
            "productEyebrow": "Product Category",
            "productPills": ["Category supply", "Integration-ready", "Project support"],
            "solutionCards": {
                "overviewEyebrow": "Overview",
                "overviewTitle": "Solution Overview",
                "challengesEyebrow": "Pain Points",
                "challengesTitle": "Customer Challenges",
                "configurationEyebrow": "Configuration",
                "configurationTitle": "Main Configuration",
                "benefitsEyebrow": "Benefits",
                "benefitsTitle": "Key Benefits",
                "supportEyebrow": "Support",
                "supportTitle": "Delivery Support",
            },
            "productCards": {
                "overviewEyebrow": "Overview",
                "overviewTitle": "Category Overview",
                "applicationsEyebrow": "Applications",
                "applicationsTitle": "Applications",
                "scopeEyebrow": "Scope",
                "scopeTitle": "Category Scope",
                "benefitsEyebrow": "Benefits",
                "benefitsTitle": "Why Buyers Choose This Category",
            },
            "caseCards": {
                "overviewEyebrow": "Overview",
                "overviewTitle": "Framework Overview",
                "needEyebrow": "Typical Need",
                "needTitle": "Typical Need",
                "designEyebrow": "Reference Design",
                "designTitle": "Reference Design",
                "configurationEyebrow": "Configuration",
                "configurationTitle": "Recommended Configuration",
                "supportEyebrow": "Support",
                "supportTitle": "Delivery Support",
                "outcomeEyebrow": "Reference Outcome",
                "outcomeTitle": "Reference Outcome",
            },
        },
        "gallery": {
            "eyebrow": "Reference Visuals",
            "title": "Typical Equipment Scope for This Framework",
            "body": "These visuals support early project discussions and will be replaced by verified customer project media when available.",
        },
        "collectionLabels": {
            "solutions": "Solutions",
            "products": "Products",
            "cases": "Reference Frameworks",
        },
    }


def build_en_locale() -> dict:
    data = load_data_js()
    return {
        "site": data["site"],
        "home": data["home"],
        "contact": build_contact_en(),
        "about": build_about_en(),
        "solutions": data["solutions"],
        "products": data["products"],
        "cases": data["cases"],
        "ui": build_ui_en(),
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    en = build_en_locale()
    write_json(LOCALES_DIR / "en.json", en)
    print(f"Wrote {LOCALES_DIR / 'en.json'}")
