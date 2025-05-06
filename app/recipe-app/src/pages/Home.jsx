import { Link } from "react-router-dom";
import "./Home.css"; 

const cards = [
  {
    title: "Search by Ingredient",
    to: "/ingredient-search",
    image: "/images/i.jpg",
  },
  {
    title: "Search by Nutrition",
    to: "/nutrition-search",
    image: "/images/n.jpg",
  },
  {
    title: "AI Recipe Suggestion",
    to: "/ai-suggestion",
    image: "/images/ai.png",
  },
];

const Home = () => {
  return (
    <div className="home-container">
      

      {/* 3 fixed-size cards side-by-side */}
      {cards.map((card, index) => (
        <Link key={index} to={card.to} className="card">
          <img src={card.image} alt={card.title} />
          <div className="card-overlay">
            <h2 className="text-2xl font-bold">{card.title}</h2>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default Home;
