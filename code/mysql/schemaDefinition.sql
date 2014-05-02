CREATE TABLE book (
    `bookId` INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `author` VARCHAR(255) NOT NULL,
    `citation` TEXT NOT NULL
) ENGINE InnoDB;

CREATE TABLE `paragraph` (
    `paraNum` INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `bookId` INT UNSIGNED NOT NULL,
    `pageNum` INT UNSIGNED NOT NULL,
    `endPageNum` INT UNSIGNED,
    `body` TEXT NOT NULL,
    FOREIGN KEY (`bookId`) REFERENCES book(`bookId`)
) ENGINE InnoDB;

CREATE TABLE `index` (
    `indexId` INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `bookId` INT UNSIGNED,
    `label` VARCHAR(200),
    `wikiLabel` VARCHAR(200),
    FOREIGN KEY (`bookId`) REFERENCES book(`bookId`)
) ENGINE InnoDB;

CREATE TABLE `indexedParagraph` (
    `indexId` INT UNSIGNED,
    `paraNum` INT UNSIGNED,
    PRIMARY KEY (`indexId`, `paraNum`),
    FOREIGN KEY (`indexId`) REFERENCES `index`(`indexId`)
) ENGINE InnoDB;

CREATE TABLE `indexedPage` (
    `indexId` INT UNSIGNED,
    `pageNum` INT UNSIGNED,
    PRIMARY KEY (`indexId`, `pageNum`),
    FOREIGN KEY (`indexId`) REFERENCES `index`(`indexId`)
) ENGINE InnoDB;

CREATE TABLE `indexToWiki` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `indexTitle` VARCHAR(200),
    `wikiTitle` VARCHAR(200)
) ENGINE InnoDB;

CREATE TABLE `articleTitles` (
    `titleId` INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(1023)
) ENGINE InnoDB;
