CREATE TABLE IF NOT EXISTS `mydb`.`LEGEND` (
  `ID` VARCHAR(45) NOT NULL,
  `CUSTOMER_NAME` VARCHAR(1000) NOT NULL DEFAULT 'CUSTOMER_NAME refers to the customer name associated with a particular transaction',
  `ASSOCIATE_NAME` VARCHAR(1000) NOT NULL DEFAULT 'ASSOCIATE_NAME refers to the same of the customer relations associate associated with a particular transaction',
  `BUY` VARCHAR(1000) NOT NULL DEFAULT 'BUY: If there is a \"y\", this was a transaction in which the preowned dealership BOUGHT a car, without making a sale',
  `TRADE` VARCHAR(1000) NOT NULL DEFAULT 'TRADE: If there is a \"y\", this is a transaction in which the preowned dealership both BOUGHT and SOLD a car',
  `SALE` VARCHAR(1000) NOT NULL DEFAULT 'SALE: If there is a \"y\", this is a transaction in which the preowned dealership only SOLD a car',
  `BUY_PRICE` VARCHAR(1000) NOT NULL DEFAULT 'BUY_PRICE: The price at which the dealership bought a preowned car',
  `TRADE_VALUE` VARCHAR(1000) NOT NULL DEFAULT 'TRADE_VALUE: The price at which the dealership bought a preowned car, during a trade',
  `STICKER` VARCHAR(1000) NOT NULL DEFAULT 'STICKER: The sticker price (original price) assigned to a car, negotiated down during a sales transaction',
  `SALE_PRICE` VARCHAR(1000) NOT NULL DEFAULT 'SALE_PRICE: The price at which the dealership sold a preowned car, either during a trade or not',
  `DATE` VARCHAR(1000) NOT NULL DEFAULT 'DATE: The data of the transaction',
  `BUY_VIN` VARCHAR(1000) NOT NULL DEFAULT 'BUY_VIN: The VIN associated with a car bought by the dealership',
  `SALE_VIN` VARCHAR(1000) NOT NULL DEFAULT 'SALE_VIN: The VIN associated with a car sold by the dealership',
  `NOTES` VARCHAR(1000) NOT NULL DEFAULT 'NOTES: Notes on the transaction, manually entered by customer relations associate',
  PRIMARY KEY (`ID`))
ENGINE = InnoDB